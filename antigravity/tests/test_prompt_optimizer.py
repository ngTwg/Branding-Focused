"""
Tests for PromptOptimizer - Token Efficiency v6.5.0-SLIM
"""

import pytest
from antigravity.core.prompt_optimizer import PromptOptimizer, OptimizationResult


@pytest.fixture
def optimizer():
    """Create prompt optimizer instance."""
    return PromptOptimizer()


def test_remove_redundant_examples(optimizer):
    """Test removing redundant examples."""
    prompt = """
Example 1: First example with some code
Example 2: Second example with more code
Example 3: Third example that's redundant
Example 4: Fourth example also redundant
"""
    
    optimized, result = optimizer.optimize(prompt)
    
    # Should keep first 2 examples, remove rest
    assert "Example 1:" in optimized
    assert "Example 2:" in optimized
    assert "Example 3:" not in optimized
    assert "Example 4:" not in optimized
    assert result.savings_percent > 0


def test_compress_instructions(optimizer):
    """Test compressing verbose instructions."""
    prompt = """
In order to complete this task, you should always make sure to verify.
It is important to note that this is critical.
Please make sure to test everything.
"""
    
    optimized, result = optimizer.optimize(prompt)
    
    # Verbose phrases should be replaced
    assert "In order to" not in optimized
    assert "To" in optimized
    assert "It is important to note that" not in optimized
    assert "Note:" in optimized
    assert "Please make sure to" not in optimized
    assert "Ensure" in optimized
    assert result.savings_percent > 0


def test_compress_whitespace(optimizer):
    """Test compressing excessive whitespace."""
    prompt = """
Line 1


Line 2



Line 3
"""
    
    optimized, result = optimizer.optimize(prompt)
    
    # Should have max 2 newlines between lines
    assert "\n\n\n" not in optimized
    assert result.savings_percent > 0


def test_remove_verbose_explanations(optimizer):
    """Test removing verbose explanations."""
    prompt = """
As you can see, this is important.
It's worth noting that we need to verify.
Basically, just do this.
"""
    
    optimized, result = optimizer.optimize(prompt)
    
    # Verbose phrases should be removed
    assert "As you can see," not in optimized
    assert "It's worth noting that" not in optimized
    assert "Basically," not in optimized
    assert result.savings_percent > 0


def test_optimization_result(optimizer):
    """Test optimization result structure."""
    prompt = "In order to test this, please make sure to verify everything."
    
    optimized, result = optimizer.optimize(prompt)
    
    assert isinstance(result, OptimizationResult)
    assert result.original_size > 0
    assert result.optimized_size > 0
    assert result.savings_bytes >= 0
    assert result.savings_percent >= 0
    assert isinstance(result.optimizations_applied, list)


def test_no_optimization_needed(optimizer):
    """Test prompt that doesn't need optimization."""
    prompt = "Short prompt."
    
    optimized, result = optimizer.optimize(prompt)
    
    # Should be unchanged or minimal change
    assert optimized == prompt or len(optimized) >= len(prompt) - 5
    assert result.savings_percent < 10


def test_complex_prompt_optimization(optimizer):
    """Test optimization of complex prompt."""
    prompt = """
# System Prompt

In order to complete this task, you should always follow these steps:

Example 1: First example
```python
def example1():
    pass
```

Example 2: Second example
```python
def example2():
    pass
```

Example 3: Third example (redundant)
```python
def example3():
    pass
```

It is important to note that you must verify everything.
Please make sure to test thoroughly.


As you can see, this is critical.
"""
    
    optimized, result = optimizer.optimize(prompt)
    
    # Should achieve significant savings
    assert result.savings_percent >= 20
    assert result.original_size > result.optimized_size
    assert len(result.optimizations_applied) > 0


def test_optimize_batch(optimizer):
    """Test batch optimization."""
    prompts = {
        "prompt1": "In order to do this, please make sure to verify.",
        "prompt2": "It is important to note that this is critical.",
        "prompt3": "As you can see, this works well.",
    }
    
    results = optimizer.optimize_batch(prompts)
    
    assert len(results) == 3
    for name, (optimized, result) in results.items():
        assert isinstance(optimized, str)
        assert isinstance(result, OptimizationResult)
        assert result.savings_percent >= 0


def test_generate_report(optimizer):
    """Test report generation."""
    prompts = {
        "prompt1": "In order to do this, please make sure to verify everything thoroughly.",
        "prompt2": "It is important to note that this is absolutely critical for success.",
    }
    
    results = optimizer.optimize_batch(prompts)
    report = optimizer.generate_report(results)
    
    assert "Prompt Optimization Report" in report
    assert "Summary" in report
    assert "Total prompts optimized: 2" in report
    assert "Original size:" in report
    assert "Optimized size:" in report
    assert "Total savings:" in report


def test_target_30_percent_savings(optimizer):
    """Test that we achieve target 30% savings on realistic prompts."""
    # Realistic verbose prompt
    prompt = """
# Task Instructions

In order to complete this task successfully, you should always make sure to follow these guidelines:

Example 1: First approach
```python
def approach1():
    # Implementation details here
    pass
```

Example 2: Second approach
```python
def approach2():
    # More implementation details
    pass
```

Example 3: Third approach (similar to first)
```python
def approach3():
    # Similar implementation
    pass
```

Example 4: Fourth approach (also similar)
```python
def approach4():
    # Another similar implementation
    pass
```

It is important to note that you must verify all inputs before processing.
Please make sure to test everything thoroughly before deployment.


As you can see, this is absolutely critical for the success of the project.
It's worth noting that we need to be very careful with edge cases.
Basically, just follow the best practices and you'll be fine.
"""
    
    optimized, result = optimizer.optimize(prompt)
    
    # Should achieve at least 30% savings
    assert result.savings_percent >= 30
    assert result.original_size > result.optimized_size
    
    # Verify optimizations were applied
    assert len(result.optimizations_applied) > 0
    
    # Verify content is still readable
    assert "Task Instructions" in optimized
    assert "Example 1:" in optimized
    assert "Example 2:" in optimized


def test_preserve_code_quality(optimizer):
    """Test that optimization preserves code quality."""
    prompt = """
Example 1: Good code
```python
def good_function():
    return True
```

Example 2: Another example
```python
def another_function():
    return False
```
"""
    
    optimized, result = optimizer.optimize(prompt)
    
    # Code blocks should be preserved
    assert "```python" in optimized
    assert "def good_function():" in optimized or "{CODE_EXAMPLE}" in optimized
    assert result.savings_percent >= 0


def test_empty_prompt(optimizer):
    """Test optimization of empty prompt."""
    prompt = ""
    
    optimized, result = optimizer.optimize(prompt)
    
    assert optimized == ""
    assert result.original_size == 0
    assert result.optimized_size == 0
    assert result.savings_percent == 0
