"""Test-wide Hypothesis settings for stable property-based execution."""

from hypothesis import HealthCheck, settings

settings.register_profile(
    "antigravity_default",
    suppress_health_check=[HealthCheck.filter_too_much],
    deadline=None,
)
settings.load_profile("antigravity_default")
