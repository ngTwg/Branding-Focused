"""
SLMRouter V3 — Pragmatic routing with validation-driven escalation.

Philosophy:
- Router is simple: default to moderate, only downgrade when certain
- Validation layer is critical: detect poor responses and escalate
- Zero harmful misclassifications: never underestimate complexity
"""

from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Literal

logger = logging.getLogger(__name__)


@dataclass
class RouteDecision:
    """Simple routing decision."""
    model: str
    complexity: Literal["simple", "moderate"]
    reasoning: str


@dataclass
class ValidationResult:
    """Response validation result."""
    is_valid: bool
    needs_escalation: bool
    reason: str


class SLMRouterV3:
    """
    Pragmatic router: simple classification + strong validation.
    
    Key principles:
    1. Default to moderate (safe)
    2. Only downgrade to simple when certain
    3. Let validation decide escalation to complex
    """
    
    # Patterns that are CLEARLY simple
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
        complex_model: str = "gemini-2.5-flash",  # Cloud for complex
    ):
        """
        Initialize pragmatic router.
        
        Args:
            simple_model: Model for simple queries
            moderate_model: Model for moderate queries (default)
            complex_model: Model for complex queries (escalation)
        """
        self.simple_model = simple_model
        self.moderate_model = moderate_model
        self.complex_model = complex_model
        
        logger.info(f"SLMRouterV3 initialized: simple={simple_model}, moderate={moderate_model}, complex={complex_model}")
    
    def classify(self, query: str) -> RouteDecision:
        """
        Classify query complexity.
        
        Logic:
        - If clearly simple → simple
        - Everything else → moderate (safe default)
        
        Args:
            query: User query
            
        Returns:
            RouteDecision
        """
        if not query or not query.strip():
            return RouteDecision(
                model=self.simple_model,
                complexity="simple",
                reasoning="Empty query",
            )
        
        query_lower = query.lower().strip()
        
        # Check if clearly simple
        is_clearly_simple = (
            any(query_lower.startswith(pattern) for pattern in self.SIMPLE_PATTERNS)
            or (len(query.split()) <= 5 and "?" in query)
        )
        
        if is_clearly_simple:
            return RouteDecision(
                model=self.simple_model,
                complexity="simple",
                reasoning="Clearly simple query (knowledge/definition)",
            )
        
        # Default to moderate (safe)
        return RouteDecision(
            model=self.moderate_model,
            complexity="moderate",
            reasoning="Default to moderate (safe)",
        )
    
    def validate_response(self, query: str, response: str) -> ValidationResult:
        """
        Validate response quality and determine if escalation needed.
        
        This is the critical component - detects poor responses.
        
        Args:
            query: Original query
            response: Model response
            
        Returns:
            ValidationResult with escalation decision
        """
        if not response or not response.strip():
            return ValidationResult(
                is_valid=False,
                needs_escalation=True,
                reason="Empty response",
            )
        
        response_lower = response.lower()
        
        # Red flag 1: Response too short
        if len(response.strip()) < 50:
            return ValidationResult(
                is_valid=False,
                needs_escalation=True,
                reason="Response too short (< 50 chars)",
            )
        
        # Red flag 2: Model admits uncertainty
        uncertainty_phrases = [
            "i don't know",
            "i'm not sure",
            "i cannot",
            "i can't help",
            "i don't have",
        ]
        if any(phrase in response_lower for phrase in uncertainty_phrases):
            return ValidationResult(
                is_valid=False,
                needs_escalation=True,
                reason="Model admits uncertainty",
            )
        
        # Red flag 3: Unclosed code blocks
        if response.count("```") % 2 != 0:
            return ValidationResult(
                is_valid=False,
                needs_escalation=True,
                reason="Unclosed code block",
            )
        
        # Red flag 4: Query has code but response doesn't
        query_has_code = (
            query.count("\n") > 10  # Multi-line query
            or "```" in query
            or any(kw in query.lower() for kw in ["def ", "class ", "function ", "import "])
        )
        response_has_code = "```" in response or "def " in response or "function " in response
        
        if query_has_code and not response_has_code:
            return ValidationResult(
                is_valid=False,
                needs_escalation=True,
                reason="Code query but no code in response",
            )
        
        # Red flag 5: Generic error messages
        error_phrases = [
            "error:",
            "exception:",
            "failed to",
            "unable to",
            "cannot process",
        ]
        # Only check first 100 chars to avoid false positives in code examples
        response_start = response_lower[:100]
        if any(phrase in response_start for phrase in error_phrases):
            return ValidationResult(
                is_valid=False,
                needs_escalation=True,
                reason="Response contains error message",
            )
        
        # Response looks good
        return ValidationResult(
            is_valid=True,
            needs_escalation=False,
            reason="Response passed validation",
        )
    
    def route_with_validation(self, query: str, response: str) -> tuple[str, str]:
        """
        Complete routing with validation and escalation.
        
        Args:
            query: User query
            response: Response from initial model
            
        Returns:
            (final_model, reason)
        """
        # Initial classification
        decision = self.classify(query)
        
        # Validate response
        validation = self.validate_response(query, response)
        
        if validation.needs_escalation:
            logger.warning(f"Escalating to complex model: {validation.reason}")
            return self.complex_model, f"Escalated: {validation.reason}"
        
        return decision.model, decision.reasoning
