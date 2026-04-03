"""
Property-based tests for LLMClient.

Feature: antigravity-architecture-upgrade
Validates: Requirements 5.6, 5.8
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from antigravity.core.llm_client import LLMClient


class TestLLMClientProperties:
    """Property tests for static prefix caching."""

    @given(
        static_prefix=st.text(min_size=100, max_size=1000),
        dynamic1=st.text(min_size=10, max_size=100),
        dynamic2=st.text(min_size=10, max_size=100),
    )
    @settings(max_examples=50)
    def test_static_prefix_invariant(self, static_prefix, dynamic1, dynamic2):
        """
        Property 15: Static Prefix Invariant.
        
        Validates: Requirements 5.6, 5.8
        
        Static prefix must remain byte-for-byte identical across multiple prompt builds.
        """
        client = LLMClient(provider="anthropic", model="claude-3-5-sonnet-20241022")
        client.set_static_prefix(static_prefix)

        # Build prompts with different dynamic suffixes
        prompt1 = client._build_system_prompt(dynamic1)
        prompt2 = client._build_system_prompt(dynamic2)

        # Extract prefix portion (assuming prefix comes first)
        if isinstance(prompt1, str):
            prefix1 = prompt1[: len(static_prefix)]
            prefix2 = prompt2[: len(static_prefix)]
        elif isinstance(prompt1, list):
            # For structured prompts (Anthropic format)
            prefix1 = prompt1[0]["text"] if prompt1 else ""
            prefix2 = prompt2[0]["text"] if prompt2 else ""
        else:
            raise TypeError(f"Unexpected prompt type: {type(prompt1)}")

        # Assert: byte-for-byte identical
        assert prefix1 == prefix2, (
            f"Static prefix not invariant:\n"
            f"Prefix 1 length: {len(prefix1)}\n"
            f"Prefix 2 length: {len(prefix2)}\n"
            f"First 100 chars of prefix1: {prefix1[:100]}\n"
            f"First 100 chars of prefix2: {prefix2[:100]}"
        )

        # Additional check: prefix should contain static_prefix content
        assert static_prefix in str(prefix1), (
            f"Static prefix not found in built prompt"
        )
