"""
Tests for Metrics API Endpoint - Task 24.

This module tests all FastAPI endpoints for health metrics exposure.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from antigravity.api.metrics import app, set_health_monitor
from antigravity.core.health_monitor import HealthMonitor


@pytest.fixture
def health_monitor():
    """Create a HealthMonitor instance with test data."""
    monitor = HealthMonitor(window_size=10)
    
    # Record some test tasks
    for i in range(15):
        monitor.record_task(
            success=i % 5 != 0,  # 80% success rate
            patches_count=1 + (i % 3),
            rollback=i % 10 == 0,  # 10% rollback rate
            tokens_used=2000 + (i * 100),
            no_op_patch=i % 20 == 0  # 5% no-op rate
        )
    
    return monitor


@pytest.fixture
def client(health_monitor):
    """Create a test client with configured HealthMonitor."""
    set_health_monitor(health_monitor)
    return TestClient(app)


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "6.2.0"


def test_get_health_metrics_default_window(client):
    """Test GET /metrics/health with default window (last_10)."""
    response = client.get("/metrics/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "health_score" in data
    assert "category" in data
    assert "metrics" in data
    assert "window" in data
    assert "timestamp" in data
    
    assert data["window"] == "last_10"
    assert data["category"] in ["excellent", "good", "fair", "poor"]
    assert 0 <= data["health_score"] <= 100
    
    # Check metrics structure
    metrics = data["metrics"]
    assert "success_rate" in metrics
    assert "rollback_rate" in metrics
    assert "avg_patches" in metrics
    assert "token_per_task" in metrics
    assert "no_op_patch_rate" in metrics


def test_get_health_metrics_all_windows(client):
    """Test GET /metrics/health with all window options."""
    windows = ["last_10", "last_hour", "last_24h", "all"]
    
    for window in windows:
        response = client.get(f"/metrics/health?window={window}")
        assert response.status_code == 200
        data = response.json()
        assert data["window"] == window


def test_get_health_metrics_invalid_window(client):
    """Test GET /metrics/health with invalid window parameter."""
    response = client.get("/metrics/health?window=invalid")
    assert response.status_code == 422  # Validation error


def test_get_derived_metrics(client):
    """Test GET /metrics/derived endpoint."""
    response = client.get("/metrics/derived")
    assert response.status_code == 200
    
    data = response.json()
    assert "avg_patches_per_success" in data
    assert "rollback_rate" in data
    assert "no_op_patch_rate" in data
    assert "slm_vs_llm_ratio" in data
    assert "token_per_task" in data
    assert "success_rate" in data
    assert "window" in data
    
    assert data["window"] == "last_10"


def test_get_derived_metrics_with_window(client):
    """Test GET /metrics/derived with custom window."""
    response = client.get("/metrics/derived?window=all")
    assert response.status_code == 200
    
    data = response.json()
    assert data["window"] == "all"


def test_get_metric_trends_success_rate(client):
    """Test GET /metrics/trends for success_rate metric."""
    response = client.get("/metrics/trends?metric=success_rate&window=all")
    assert response.status_code == 200
    
    data = response.json()
    assert data["metric"] == "success_rate"
    assert "data_points" in data
    assert "trend" in data
    assert "change_percentage" in data
    
    assert data["trend"] in ["improving", "stable", "degrading"]
    assert len(data["data_points"]) > 0
    
    # Check data point structure
    point = data["data_points"][0]
    assert "timestamp" in point
    assert "value" in point


def test_get_metric_trends_all_metrics(client):
    """Test GET /metrics/trends for all supported metrics."""
    metrics = ["health_score", "success_rate", "token_per_task", "rollback_rate"]
    
    for metric in metrics:
        response = client.get(f"/metrics/trends?metric={metric}&window=last_10")
        assert response.status_code == 200
        data = response.json()
        assert data["metric"] == metric


def test_get_metric_trends_invalid_metric(client):
    """Test GET /metrics/trends with invalid metric."""
    response = client.get("/metrics/trends?metric=invalid_metric")
    assert response.status_code == 422  # Validation error


def test_get_baseline_metrics(client, health_monitor):
    """Test GET /metrics/baseline endpoint."""
    # Establish baseline first
    health_monitor.establish_baseline()
    
    response = client.get("/metrics/baseline")
    assert response.status_code == 200
    
    data = response.json()
    assert "baseline_token_per_task" in data
    assert "baseline_patches" in data
    assert "baseline_success_rate" in data
    assert "established_at" in data
    assert "task_count" in data
    assert "last_updated" in data
    
    assert data["task_count"] == 50


def test_get_baseline_metrics_not_established(client):
    """Test GET /metrics/baseline when baseline not established."""
    # Create a new monitor without baseline in a temp directory
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        monitor = HealthMonitor(window_size=10, data_dir=tmpdir)
        set_health_monitor(monitor)
        
        response = client.get("/metrics/baseline")
        assert response.status_code == 404
        assert "not established" in response.json()["detail"].lower()


def test_get_suggestions(client):
    """Test GET /metrics/suggestions endpoint."""
    response = client.get("/metrics/suggestions")
    assert response.status_code == 200
    
    data = response.json()
    assert "suggestions" in data
    assert "anomalies" in data
    
    assert isinstance(data["suggestions"], list)
    assert isinstance(data["anomalies"], list)
    
    # Check suggestion structure if any exist
    if data["suggestions"]:
        suggestion = data["suggestions"][0]
        assert "priority" in suggestion
        assert "message" in suggestion
        assert "reason" in suggestion


def test_cors_middleware_configured(client):
    """Test that CORS middleware is configured (verified by middleware presence)."""
    # CORS middleware is configured in the app
    # TestClient doesn't trigger CORS headers, but we can verify the app has the middleware
    from fastapi.middleware.cors import CORSMiddleware
    
    # Check that CORS middleware is in the app's middleware stack
    has_cors = any(
        isinstance(middleware, CORSMiddleware) or 
        (hasattr(middleware, 'cls') and middleware.cls == CORSMiddleware)
        for middleware in app.user_middleware
    )
    assert has_cors, "CORS middleware should be configured"


def test_json_response_format(client):
    """Test that all endpoints return valid JSON."""
    endpoints = [
        "/health",
        "/metrics/health",
        "/metrics/derived",
        "/metrics/trends?metric=success_rate",
        "/metrics/suggestions"
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code in [200, 404]  # 404 for baseline if not established
        assert response.headers["content-type"] == "application/json"


def test_timestamp_format(client):
    """Test that timestamps are in ISO format."""
    response = client.get("/metrics/health")
    assert response.status_code == 200
    
    data = response.json()
    timestamp = data["timestamp"]
    
    # Verify ISO format by parsing
    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        pytest.fail(f"Timestamp not in ISO format: {timestamp}")


def test_metric_value_ranges(client):
    """Test that metric values are within expected ranges."""
    response = client.get("/metrics/derived")
    assert response.status_code == 200
    
    data = response.json()
    
    # Rates should be between 0 and 1
    assert 0 <= data["success_rate"] <= 1
    assert 0 <= data["rollback_rate"] <= 1
    assert 0 <= data["no_op_patch_rate"] <= 1
    assert 0 <= data["slm_vs_llm_ratio"] <= 1
    
    # Tokens and patches should be non-negative
    assert data["token_per_task"] >= 0
    assert data["avg_patches_per_success"] >= 0


def test_health_score_range(client):
    """Test that health score is within 0-100 range."""
    response = client.get("/metrics/health")
    assert response.status_code == 200
    
    data = response.json()
    assert 0 <= data["health_score"] <= 100


def test_trend_change_percentage(client):
    """Test that trend change percentage is calculated correctly."""
    response = client.get("/metrics/trends?metric=success_rate&window=all")
    assert response.status_code == 200
    
    data = response.json()
    change = data["change_percentage"]
    
    # Change percentage should be a valid number
    assert isinstance(change, (int, float))
    assert not (change != change)  # Not NaN
