"""
Property-based tests for LLMClient (Architecture Upgrade).

Feature: antigravity-architecture-upgrade
Tests static prefix invariant using Hypothesis.
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from unittest.mock import Mock, MagicMock

from core.llm_client import LLMClient


# Feature: antigravity-architecture-upgrade, Property 15: Static Prefix Invariant
@given(
    static_prefix=st.text(min_size=100, max_size=1000),
    dynamic1=st.text(min_size=10, max_size=100),
    dynamic2=st.text(min_size=10, max_size=100),
)
@settings(max_examples=30)
def test_static_prefix_invariant(static_prefix, dynamic1, dynamic2):
    """
    Property 15: Static Prefix Invariant
    Validates: Requirements 5.6, 5.8
    
    Verify that static prefix remains identical across multiple prompt builds.
    """
    # Create LLMClient with mocked API
    client = LLMClient(
        provider="anthropic",
        model="claude-3-5-sonnet-20241022",
        api_key="test-key"
    )
    
    # Set static prefix
    client.set_static_prefix(static_prefix)
    
    # Build prompts with different dynamic suffixes
    prompt1 = client._build_system_prompt(dynamic1)
    prompt2 = client._build_system_prompt(dynamic2)
    
    # Extract prefix portions
    # For Anthropic, prompt is a list of dicts with cache_control
    if isinstance(prompt1, list):
        prefix1 = prompt1[0]["text"] if len(prompt1) > 0 else ""
        prefix2 = prompt2[0]["text"] if len(prompt2) > 0 else ""
    else:
        # For other providers, it's a string
        prefix1 = prompt1.split(dynamic1)[0] if dynamic1 in prompt1 else prompt1
        prefix2 = prompt2.split(dynamic2)[0] if dynamic2 in prompt2 else prompt2
    
    # Assert: Prefix identical byte-for-byte
    assert prefix1 == prefix2, (
        f"Static prefix not invariant:\n"
        f"Prefix 1 length: {len(prefix1)}\n"
        f"Prefix 2 length: {len(prefix2)}\n"
        f"First 100 chars differ: {prefix1[:100] != prefix2[:100]}"
    )
