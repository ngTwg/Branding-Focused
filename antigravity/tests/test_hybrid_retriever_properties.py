"""
Property-based tests for HybridRetriever.

Feature: antigravity-architecture-upgrade
Validates: Requirements 1.2, 1.3, 1.4, 1.9, 1.11
"""

from hypothesis import assume, given, settings
from hypothesis import strategies as st

from antigravity.core.hybrid_retriever import HybridRetriever
from antigravity.core.schemas import SkillDocument


class TestHybridRetrieverProperties:
    """Property tests for hybrid retrieval scoring and ranking."""

    @staticmethod
    def _create_sample_skills():
        """Create sample skills for testing."""
        return [
            SkillDocument(
                skill_id="frontend-react",
                content="React hooks useState useEffect component lifecycle",
                domain_tags=["frontend"],
                tier=1,
            ),
            SkillDocument(
                skill_id="backend-api",
                content="REST API design endpoints authentication authorization",
                domain_tags=["backend"],
                tier=2,
            ),
            SkillDocument(
                skill_id="security-owasp",
                content="OWASP Top 10 XSS SQL injection CSRF security vulnerabilities",
                domain_tags=["security"],
                tier=2,
            ),
            SkillDocument(
                skill_id="workflows-debug",
                content="Systematic debugging reproduce isolate fix verify test",
                domain_tags=["workflows"],
                tier=1,
            ),
        ]

    @given(
        query=st.text(min_size=3, max_size=100),
        alpha=st.floats(0, 1),
        beta=st.floats(0, 1),
    )
    @settings(max_examples=50)
    def test_score_normalization_and_ranking_invariant(self, query, alpha, beta):
        """
        Property 1: Score Normalization và Ranking Invariant.
        
        Validates: Requirements 1.2, 1.3
        
        All final_scores must be in [0,1] and results must be sorted descending.
        """
        assume(abs(alpha + beta - 1.0) < 0.01)  # Ensure alpha + beta ≈ 1

        retriever = HybridRetriever(skills_dir=None, alpha=alpha, beta=beta)
        retriever.index(self._create_sample_skills())

        results = retriever.retrieve(query, top_k=5)

        # Assert: scores in [0,1]
        for skill in results:
            assert 0 <= skill.final_score <= 1, (
                f"Score out of range: {skill.final_score} for skill {skill.skill_id}"
            )

        # Assert: sorted descending
        scores = [skill.final_score for skill in results]
        assert scores == sorted(scores, reverse=True), (
            f"Results not sorted: {scores}"
        )

    @given(
        query=st.text(min_size=3, max_size=100),
        alpha1=st.floats(0, 0.5),
        alpha2=st.floats(0.5, 1),
    )
    @settings(max_examples=50)
    def test_alpha_beta_monotonicity(self, query, alpha1, alpha2):
        """
        Property 2: Monotonicity của Alpha/Beta Weights.
        
        Validates: Requirements 1.9
        
        Increasing alpha should increase BM25 contribution to final score.
        """
        beta1 = 1 - alpha1
        beta2 = 1 - alpha2

        retriever1 = HybridRetriever(skills_dir=None, alpha=alpha1, beta=beta1)
        retriever1.index(self._create_sample_skills())
        results1 = retriever1.retrieve(query, top_k=3)

        retriever2 = HybridRetriever(skills_dir=None, alpha=alpha2, beta=beta2)
        retriever2.index(self._create_sample_skills())
        results2 = retriever2.retrieve(query, top_k=3)

        # Calculate BM25 contribution (alpha * bm25_norm)
        if results1 and results2:
            contrib1 = sum(alpha1 * r.bm25_norm for r in results1) / len(results1)
            contrib2 = sum(alpha2 * r.bm25_norm for r in results2) / len(results2)

            # Assert: higher alpha → higher BM25 contribution
            assert contrib2 >= contrib1, (
                f"Alpha monotonicity violated: alpha1={alpha1}, contrib1={contrib1}, "
                f"alpha2={alpha2}, contrib2={contrib2}"
            )

    @given(domain=st.sampled_from(["frontend", "backend", "security", "workflows"]))
    @settings(max_examples=20)
    def test_domain_filter_containment(self, domain):
        """
        Property 3: Domain Filter Containment.
        
        Validates: Requirements 1.4
        
        All results must belong to the specified domain when filter is applied.
        """
        retriever = HybridRetriever(skills_dir=None)
        retriever.index(self._create_sample_skills())

        results = retriever.retrieve("test query", domain_filter=domain, top_k=5)

        # Assert: all results contain domain tag
        for skill in results:
            assert domain in skill.domain_tags, (
                f"Domain filter violated: skill {skill.skill_id} has tags {skill.domain_tags}, "
                f"expected {domain}"
            )

    @given(
        query=st.text(min_size=3, max_size=100),
        n_runs=st.integers(2, 5),
    )
    @settings(max_examples=30)
    def test_deterministic_tie_breaking(self, query, n_runs):
        """
        Property 4: Deterministic Tie-Breaking.
        
        Validates: Requirements 1.11
        
        Multiple runs with same query must return identical ordering.
        """
        retriever = HybridRetriever(skills_dir=None)
        retriever.index(self._create_sample_skills())

        runs = []
        for _ in range(n_runs):
            results = retriever.retrieve(query, top_k=5)
            runs.append([skill.skill_id for skill in results])

        # Assert: all runs identical
        for i in range(len(runs) - 1):
            assert runs[i] == runs[i + 1], (
                f"Tie-breaking not deterministic:\n"
                f"Run {i}: {runs[i]}\n"
                f"Run {i+1}: {runs[i+1]}"
            )
