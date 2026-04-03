"""
Property-based tests for TracingService.

Feature: antigravity-architecture-upgrade
Validates: Requirements 6.2, 6.5
"""

from unittest.mock import MagicMock, patch

from hypothesis import given, settings
from hypothesis import strategies as st

from antigravity.core.tracing import TracingService


class TestTracingProperties:
    """Property tests for trace completeness."""

    @given(
        model=st.text(min_size=1, max_size=50),
        input_tokens=st.one_of(st.none(), st.integers(0, 10000)),
        output_tokens=st.one_of(st.none(), st.integers(0, 10000)),
        latency_ms=st.one_of(st.none(), st.floats(0, 10000)),
        task_name=st.text(min_size=1, max_size=100),
    )
    @settings(max_examples=100)
    def test_trace_fields_completeness(
        self, model, input_tokens, output_tokens, latency_ms, task_name
    ):
        """
        Property 16: Trace Fields Completeness.
        
        Validates: Requirements 6.2, 6.5
        
        All trace fields must be logged, including optional None values.
        """
        with patch("antigravity.core.tracing.Langfuse") as mock_langfuse:
            mock_client = MagicMock()
            mock_trace = MagicMock()
            mock_span = MagicMock()

            mock_langfuse.return_value = mock_client
            mock_client.trace.return_value = mock_trace
            mock_trace.span.return_value = mock_span

            # Initialize tracing with mocked Langfuse
            tracer = TracingService(session_id="test-session", notebook_id="test-notebook")
            tracer._client = mock_client
            tracer._trace = mock_trace

            # Log generation
            tracer.log_generation(
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms,
                task_name=task_name,
            )

            # Verify span was called
            assert mock_trace.span.called, "Span not created"

            # Get the call arguments
            call_kwargs = mock_trace.span.call_args[1] if mock_trace.span.call_args else {}

            # Assert: required fields present
            assert "name" in call_kwargs, "Missing 'name' field"
            assert call_kwargs["name"] == task_name, f"Task name mismatch: {call_kwargs['name']} != {task_name}"

            # Assert: metadata contains model
            if "metadata" in call_kwargs:
                metadata = call_kwargs["metadata"]
                assert "model" in metadata, "Missing 'model' in metadata"
                assert metadata["model"] == model, f"Model mismatch: {metadata['model']} != {model}"

                # Check optional fields are present (even if None)
                assert "input_tokens" in metadata, "Missing 'input_tokens' in metadata"
                assert "output_tokens" in metadata, "Missing 'output_tokens' in metadata"
                assert "latency_ms" in metadata, "Missing 'latency_ms' in metadata"

                # Verify values match (including None)
                assert metadata["input_tokens"] == input_tokens, (
                    f"input_tokens mismatch: {metadata['input_tokens']} != {input_tokens}"
                )
                assert metadata["output_tokens"] == output_tokens, (
                    f"output_tokens mismatch: {metadata['output_tokens']} != {output_tokens}"
                )
                assert metadata["latency_ms"] == latency_ms, (
                    f"latency_ms mismatch: {metadata['latency_ms']} != {latency_ms}"
                )
