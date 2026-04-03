"""
SLMRouter — Intent classification using sentence-transformers.

Classifies user intent via cosine similarity with prototype embeddings to save LLM calls.
Operates with <100ms latency on CPU and gracefully degrades if sentence-transformers unavailable.

Validates Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8
Task 6.2: Cascading logic for reasoning models
Task 2 (Final Polish): Budget-aware routing with graceful degradation
"""

from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Optional, Literal

from .schemas import SLMRouteDecision, ModelCandidate, BudgetAwareRoutingDecision
from .budget_guard import BudgetGuard, BudgetExceededError

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:
    SentenceTransformer = None

try:
    import numpy as np
except Exception:
    np = None


class SLMRouter:
    """
    Intent classifier using cosine similarity with prototype embeddings.
    
    Features:
    - Classify via sentence-transformers (all-MiniLM-L6-v2 by default)
    - Configurable confidence threshold (default: 0.85)
    - Hot-reload prototypes without restart
    - Graceful degradation if sentence-transformers unavailable
    - <100ms latency on CPU
    - Idempotent: classify(x) == classify(classify(x).chosen)
    - Task 6.2: Cascading logic for reasoning models
    - Task 2: Budget-aware routing with graceful degradation
    """
    
    # Task 6.2: Complexity thresholds for cascading
    COMPLEXITY_THRESHOLDS = {
        "simple": 0.85,      # High confidence → simple task → Sonnet
        "moderate": 0.70,    # Medium confidence → moderate task → Sonnet
        "complex": 0.50,     # Low confidence → complex task → o1-mini
    }
    
    # Task 6.2: Complexity indicators (keywords that suggest complex reasoning)
    COMPLEX_INDICATORS = [
        "debug", "fix bug", "investigate", "analyze", "optimize",
        "refactor", "architecture", "design pattern", "algorithm",
        "performance", "security", "complex", "difficult", "tricky",
        "multi-step", "reasoning", "logic", "proof", "verify",
    ]
    
    # Task 2: Model cost estimates (tokens per call)
    MODEL_COSTS = {
        "o1-mini": {
            "estimated_tokens": 5000,
            "quality_tier": "high",
            "is_local": False,
        },
        "claude-3-5-sonnet-20241022": {
            "estimated_tokens": 2000,
            "quality_tier": "high",
            "is_local": False,
        },
        "qwen2.5:3b-instruct": {
            "estimated_tokens": 1000,
            "quality_tier": "medium",
            "is_local": True,
        },
    }
    
    # Task 2: Model ranking by complexity (best to worst for each tier)
    MODEL_RANKING = {
        "complex": ["o1-mini", "claude-3-5-sonnet-20241022", "qwen2.5:3b-instruct"],
        "moderate": ["claude-3-5-sonnet-20241022", "qwen2.5:3b-instruct"],
        "simple": ["claude-3-5-sonnet-20241022", "qwen2.5:3b-instruct"],
    }

    def __init__(
        self,
        prototypes_path: Path | str | None,
        confidence_threshold: float = 0.85,
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        """
        Initialize SLMRouter.
        
        Args:
            prototypes_path: Path to JSON file containing prototype embeddings
            confidence_threshold: Minimum confidence to return classification (default: 0.85)
            embedding_model: sentence-transformers model name (default: all-MiniLM-L6-v2)
        
        Graceful degradation: If sentence-transformers fails to load, _enabled=False
        """
        self.prototypes_path = Path(prototypes_path) if prototypes_path else Path("__slm_prototypes_missing__.json")
        self.confidence_threshold = confidence_threshold
        self.embedding_model_name = embedding_model
        
        self._enabled = False
        self._model = None
        self._prototypes = {}
        self._prototype_embeddings = None
        
        # Try to load sentence-transformers
        try:
            if SentenceTransformer is None or np is None:
                raise ImportError("sentence-transformers and/or numpy unavailable")
            
            self._SentenceTransformer = SentenceTransformer
            self._np = np
            
            # Load model
            self._model = SentenceTransformer(embedding_model)
            self._enabled = True
            logger.info(f"SLMRouter initialized with model: {embedding_model}")
            
            # Load prototypes
            self._load_prototypes()
            
        except ImportError as e:
            logger.warning(
                f"sentence-transformers not available: {e}. "
                "SLMRouter disabled, will fall through to LLM routing."
            )
            self._enabled = False
        except Exception as e:
            logger.error(f"Failed to initialize SLMRouter: {e}. Disabling.")
            self._enabled = False

    def _load_prototypes(self) -> None:
        """
        Load prototype embeddings from JSON file.
        
        Expected JSON format:
        {
            "frontend": {
                "examples": ["create react component", "style button", ...],
                "embedding": [0.1, 0.2, ...]  # optional pre-computed
            },
            "backend": {...},
            ...
        }
        """
        if not self.prototypes_path.exists():
            logger.warning(f"Prototypes file not found: {self.prototypes_path}. SLMRouter disabled.")
            self._enabled = False
            return
        
        try:
            with open(self.prototypes_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self._prototypes = data
            
            # Compute embeddings for each category
            embeddings = []
            categories = []
            
            for category, proto_data in data.items():
                if isinstance(proto_data, dict):
                    # If pre-computed embedding exists, use it
                    if "embedding" in proto_data:
                        embedding = self._np.array(proto_data["embedding"])
                    else:
                        # Otherwise compute from examples
                        examples = proto_data.get("examples", [])
                        if not examples:
                            logger.warning(f"No examples for category '{category}', skipping")
                            continue
                        # Average embeddings of all examples
                        example_embeddings = self._model.encode(examples)
                        embedding = self._np.mean(example_embeddings, axis=0)
                    
                    embeddings.append(embedding)
                    categories.append(category)
            
            if embeddings:
                self._prototype_embeddings = self._np.array(embeddings)
                self._categories = categories
                logger.info(f"Loaded {len(categories)} prototype categories: {categories}")
            else:
                logger.warning("No valid prototypes loaded. SLMRouter disabled.")
                self._enabled = False
                
        except Exception as e:
            logger.error(f"Failed to load prototypes from {self.prototypes_path}: {e}")
            self._enabled = False

    def reload_prototypes(self) -> None:
        """
        Hot-reload prototypes from JSON file without restart.
        
        Validates Requirement 4.4: reload without restart
        """
        if not self._enabled:
            logger.warning("SLMRouter is disabled, cannot reload prototypes")
            return
        
        logger.info(f"Reloading prototypes from {self.prototypes_path}")
        self._load_prototypes()
    
    def assess_complexity(self, query: str) -> Literal["simple", "moderate", "complex"]:
        """
        Assess task complexity based on query content.
        
        Args:
            query: User query string
            
        Returns:
            "simple", "moderate", or "complex"
            
        Validates: Task 6.2 - Complexity assessment for cascading
        """
        if not query:
            return "simple"
        
        query_lower = query.lower()
        
        # Count complexity indicators
        indicator_count = sum(1 for indicator in self.COMPLEX_INDICATORS if indicator in query_lower)
        
        # Check query length (longer queries often indicate complexity)
        word_count = len(query.split())
        
        # Heuristic scoring
        complexity_score = 0.0
        
        # Indicator-based scoring (more weight on indicators)
        if indicator_count >= 3:
            complexity_score += 0.7  # Increased from 0.5
        elif indicator_count >= 2:
            complexity_score += 0.5  # New threshold
        elif indicator_count >= 1:
            complexity_score += 0.25  # Reduced from 0.3
        
        # Length-based scoring
        if word_count > 50:
            complexity_score += 0.3
        elif word_count > 20:
            complexity_score += 0.2
        elif word_count > 10:
            complexity_score += 0.1
        
        # Classify based on score
        if complexity_score >= 0.6:
            return "complex"
        elif complexity_score >= 0.3:
            return "moderate"
        else:
            return "simple"
    
    def recommend_model(self, query: str, confidence: float | None = None) -> str:
        """
        Recommend model based on task complexity and confidence.
        
        Args:
            query: User query string
            confidence: Classification confidence (if available)
            
        Returns:
            Recommended model name ("claude-3-5-sonnet-20241022" or "o1-mini")
            
        Validates: Task 6.2 - Cascading logic
        """
        complexity = self.assess_complexity(query)
        
        # If we have confidence, use it to refine the decision
        if confidence is not None:
            if confidence >= self.COMPLEXITY_THRESHOLDS["simple"]:
                # High confidence → simple task → Sonnet
                return "claude-3-5-sonnet-20241022"
            elif confidence >= self.COMPLEXITY_THRESHOLDS["moderate"]:
                # Medium confidence → moderate task → Sonnet
                return "claude-3-5-sonnet-20241022"
            else:
                # Low confidence → complex task → o1-mini
                return "o1-mini"
        
        # Fallback to complexity-based decision
        if complexity == "complex":
            return "o1-mini"
        else:
            return "claude-3-5-sonnet-20241022"
    
    def route_with_budget(
        self,
        query: str,
        budget_guard: BudgetGuard,
        confidence: float | None = None,
    ) -> BudgetAwareRoutingDecision:
        """
        Route to model that fits within budget with graceful degradation.
        
        Args:
            query: User query string
            budget_guard: BudgetGuard instance to check remaining budget
            confidence: Classification confidence (if available)
            
        Returns:
            BudgetAwareRoutingDecision with chosen model and metadata
            
        Raises:
            BudgetExceededError: If no model fits within budget
            
        Validates: Task 2 - Budget-aware routing
        
        Properties:
        - P1 (Budget Respect): chosen model always has estimated_cost <= remaining_budget
        - P2 (Graceful Degradation): fallback to cheaper models when budget constrained
        - P3 (Quality Monotonicity): prefer expensive models for complex tasks unless budget forces fallback
        """
        # 1. Assess complexity
        complexity = self.assess_complexity(query)
        
        # 2. Get remaining budget
        budget_status = budget_guard.get_status()
        remaining_tokens = budget_status.tokens_remaining
        
        # 3. Rank models by preference for this complexity
        candidates_ranked = self.MODEL_RANKING.get(complexity, self.MODEL_RANKING["moderate"])
        
        # 4. Build candidate list with cost info
        candidates = []
        for model_name in candidates_ranked:
            if model_name in self.MODEL_COSTS:
                cost_info = self.MODEL_COSTS[model_name]
                candidates.append(
                    ModelCandidate(
                        name=model_name,
                        estimated_tokens=cost_info["estimated_tokens"],
                        quality_tier=cost_info["quality_tier"],
                        is_local=cost_info["is_local"],
                    )
                )
        
        # 5. Select first model that fits budget
        for i, candidate in enumerate(candidates):
            if candidate.estimated_tokens <= remaining_tokens:
                is_fallback = i > 0  # Fallback if not the first choice
                
                reason = f"{complexity} task"
                if is_fallback:
                    reason += f", budget-constrained fallback (remaining: {remaining_tokens} tokens)"
                else:
                    reason += f", optimal choice (remaining: {remaining_tokens} tokens)"
                
                logger.info(
                    f"Budget-aware routing: {candidate.name} "
                    f"(cost: {candidate.estimated_tokens}, remaining: {remaining_tokens}, "
                    f"complexity: {complexity}, fallback: {is_fallback})"
                )
                
                return BudgetAwareRoutingDecision(
                    model=candidate.name,
                    reason=reason,
                    estimated_cost=candidate.estimated_tokens,
                    is_fallback=is_fallback,
                    complexity=complexity,
                    candidates_considered=candidates,
                )
        
        # 6. No model fits budget - raise error
        cheapest = candidates[-1] if candidates else None
        if cheapest:
            raise BudgetExceededError(
                f"Budget exhausted: need {cheapest.estimated_tokens} tokens, "
                f"only {remaining_tokens} remaining",
                "tokens"
            )
        else:
            raise BudgetExceededError(
                f"No models available for complexity '{complexity}'",
                "tokens"
            )

    def classify(self, query: str) -> Optional[SLMRouteDecision]:
        """
        Classify user intent using cosine similarity with prototypes.
        
        Args:
            query: User query string
        
        Returns:
            SLMRouteDecision if confidence >= threshold, else None
            None if _enabled=False (graceful degradation)
        
        Validates Requirements:
        - 4.1: Classify using sentence-transformers cosine similarity
        - 4.2: Return result if confidence >= threshold
        - 4.3: Return None if confidence < threshold (fall through to LLM)
        - 4.6: Return None if _enabled=False (graceful degradation)
        - 4.7: Log routing decisions
        - 4.8: Idempotent classification
        """
        if not self._enabled:
            return None
        
        if not query or not query.strip():
            logger.warning("Empty query provided to SLMRouter")
            return None
        
        try:
            # Encode query
            query_embedding = self._model.encode([query])[0]
            
            # Compute cosine similarity with all prototypes
            # cosine_similarity = dot(a, b) / (norm(a) * norm(b))
            query_norm = self._np.linalg.norm(query_embedding)
            prototype_norms = self._np.linalg.norm(self._prototype_embeddings, axis=1)
            
            dot_products = self._np.dot(self._prototype_embeddings, query_embedding)
            similarities = dot_products / (prototype_norms * query_norm + 1e-8)
            
            # Get top-k results
            top_k_indices = self._np.argsort(similarities)[::-1]
            top_k_scores = similarities[top_k_indices]
            
            # Build top_k list
            top_k = [
                {"label": self._categories[idx], "score": float(score)}
                for idx, score in zip(top_k_indices, top_k_scores)
            ]
            
            # Get best match
            best_idx = top_k_indices[0]
            best_category = self._categories[best_idx]
            best_confidence = float(top_k_scores[0])
            
            # Log decision
            log_data = {
                "chosen": best_category,
                "confidence": best_confidence,
                "top_k": top_k[:5],  # Log top 5
            }
            logger.info(f"SLMRouter decision: {json.dumps(log_data)}")
            
            # Check threshold
            if best_confidence >= self.confidence_threshold:
                return SLMRouteDecision(
                    chosen=best_category,
                    confidence=best_confidence,
                    top_k=top_k[:5],
                    llm_fallback_triggered=False,
                )
            else:
                logger.info(
                    f"Confidence {best_confidence:.3f} below threshold {self.confidence_threshold}, "
                    "falling through to LLM"
                )
                return None
                
        except Exception as e:
            logger.error(f"Error during SLMRouter classification: {e}", exc_info=True)
            return None


# ── SLMRouterV3: Pragmatic Validation-Driven Routing (Merged from v3) ───────

from dataclasses import dataclass
from typing import Literal as _Literal


@dataclass
class RouteDecisionV3:
    """Simple routing decision from V3 router."""
    model: str
    complexity: _Literal["simple", "moderate"]
    reasoning: str


@dataclass
class ValidationResult:
    """Response validation result — detects poor responses for escalation."""
    is_valid: bool
    needs_escalation: bool
    reason: str


class SLMRouterV3:
    """
    Pragmatic router: simple classification + strong validation.
    Merged from slm_router_v3.py (now deleted).

    Key principles:
    1. Default to moderate (safe)
    2. Only downgrade to simple when certain
    3. Let validation decide escalation to complex
    """

    SIMPLE_PATTERNS = [
        "what is ",
        "what does ",
        "what's ",
        "explain ",
        "define ",
        "tell me about ",
        "how do i install ",
        "difference between ",
    ]

    def __init__(
        self,
        simple_model: str = "smollm2:1.7b",
        moderate_model: str = "qwen2.5:3b-instruct",
        complex_model: str = "gemini-2.5-flash",
    ):
        self.simple_model = simple_model
        self.moderate_model = moderate_model
        self.complex_model = complex_model
        logger.info(
            f"SLMRouterV3 initialized: simple={simple_model}, "
            f"moderate={moderate_model}, complex={complex_model}"
        )

    def classify(self, query: str) -> RouteDecisionV3:
        """Classify query: clearly simple → simple, everything else → moderate (safe)."""
        if not query or not query.strip():
            return RouteDecisionV3(model=self.simple_model, complexity="simple", reasoning="Empty query")

        query_lower = query.lower().strip()
        is_clearly_simple = (
            any(query_lower.startswith(p) for p in self.SIMPLE_PATTERNS)
            or (len(query.split()) <= 5 and "?" in query)
        )

        if is_clearly_simple:
            return RouteDecisionV3(
                model=self.simple_model,
                complexity="simple",
                reasoning="Clearly simple query (knowledge/definition)",
            )
        return RouteDecisionV3(model=self.moderate_model, complexity="moderate", reasoning="Default to moderate (safe)")

    def validate_response(self, query: str, response: str) -> ValidationResult:
        """Validate response quality; escalate to complex model if poor."""
        if not response or not response.strip():
            return ValidationResult(is_valid=False, needs_escalation=True, reason="Empty response")

        response_lower = response.lower()

        if len(response.strip()) < 50:
            return ValidationResult(is_valid=False, needs_escalation=True, reason="Response too short (<50 chars)")

        uncertainty = ["i don't know", "i'm not sure", "i cannot", "i can't help", "i don't have"]
        if any(p in response_lower for p in uncertainty):
            return ValidationResult(is_valid=False, needs_escalation=True, reason="Model admits uncertainty")

        if response.count("```") % 2 != 0:
            return ValidationResult(is_valid=False, needs_escalation=True, reason="Unclosed code block")

        query_has_code = (
            query.count("\n") > 10
            or "```" in query
            or any(kw in query.lower() for kw in ["def ", "class ", "function ", "import "])
        )
        response_has_code = "```" in response or "def " in response or "function " in response
        if query_has_code and not response_has_code:
            return ValidationResult(is_valid=False, needs_escalation=True, reason="Code query but no code in response")

        error_start = response_lower[:100]
        if any(p in error_start for p in ["error:", "exception:", "failed to", "unable to", "cannot process"]):
            return ValidationResult(is_valid=False, needs_escalation=True, reason="Response contains error message")

        return ValidationResult(is_valid=True, needs_escalation=False, reason="Response passed validation")

    def route_with_validation(self, query: str, response: str) -> tuple[str, str]:
        """Full routing + validation + escalation. Returns (model, reason)."""
        decision = self.classify(query)
        validation = self.validate_response(query, response)
        if validation.needs_escalation:
            logger.warning(f"Escalating to complex model: {validation.reason}")
            return self.complex_model, f"Escalated: {validation.reason}"
        return decision.model, decision.reasoning
