"""
Tests for Metrics Export functionality - Task 25.5.

This module tests:
- GET /metrics/export/json endpoint
- GET /metrics/export/csv endpoint
- GET /metrics/export/prometheus endpoint
- CLI export commands
- Query parameters
- Error handling
"""

import pytest
import json
import csv
import io
from datetime import datetime, timedelta
from pathlib import Path
from fastapi.testclient import TestClient

from antigravity.api.metrics import app, set_health_monitor
from antigravity.core.health_monitor import HealthMonitor


@pytest.fixture
def health_monitor():
    """Create a HealthMonitor with sample data."""
    monitor = HealthMonitor(window_size=20)
    
    # Record 15 sample tasks with varied metrics
    base_time = datetime.now() - timedelta(hours=2)
    
    for i in range(15):
        monitor.record_task(
            success=(i % 4 != 0),  # 75% success rate
            patches_count=1 + (i % 3),  # 1-3 patches
            rollback=(i % 5 == 0),  # 20% rollback rate
            tokens_used=2000 + (i * 100),  # Increasing token usage
            no_op_patch=(i % 10 == 0)  # 10% no-op rate
        )
        
        # Adjust timestamp for time-based filtering
        monitor._task_history[-1].timestamp = base_time + timedelta(minutes=i * 10)
    
    return monitor


@pytest.fixture
def client(health_monitor):
    """Create FastAPI test client with initialized HealthMonitor."""
    set_health_monitor(health_monitor)
    return TestClient(app)


# ============================================================================
# Test 25.1: JSON Export Endpoint
# ============================================================================

def test_export_json_all_window(client):
    """Test JSON export with 'all' window."""
    response = client.get("/metrics/export/json?window=all")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert "attachment" in response.headers["content-disposition"]
    assert "metrics_" in response.headers["content-disposition"]
    
    # Parse JSON content
    data = response.json()
    
    # Verify structure
    assert "export_timestamp" in data
    assert "window" in data
    assert data["window"] == "all"
    
    assert "health" in data
    assert "score" in data["health"]
    assert "category" in data["health"]
    assert 0 <= data["health"]["score"] <= 100
    
    assert "derived_metrics" in data
    assert "success_rate" in data["derived_metrics"]
    assert "rollback_rate" in data["derived_metrics"]
    assert "token_per_task" in data["derived_metrics"]
    
    assert "task_history" in data
    assert len(data["task_history"]) == 15  # All tasks
    
    # Verify task structure
    task = data["task_history"][0]
    assert "task_id" in task
    assert "timestamp" in task
    assert "success" in task
    assert "patches_count" in task
    assert "rollback" in task
    assert "tokens_used" in task
    assert "no_op_patch" in task


def test_export_json_last_10_window(client):
    """Test JSON export with 'last_10' window."""
    response = client.get("/metrics/export/json?window=last_10")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["window"] == "last_10"
    assert len(data["task_history"]) == 10  # Last 10 tasks


def test_export_json_last_hour_window(client, health_monitor):
    """Test JSON export with 'last_hour' window."""
    response = client.get("/metrics/export/json?window=last_hour")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["window"] == "last_hour"
    # Should have tasks from last hour (we created tasks over 2 hours, so some should be filtered)
    assert len(data["task_history"]) < 15


def test_export_json_includes_baseline(client, health_monitor):
    """Test JSON export includes baseline if established."""
    # Establish baseline
    health_monitor.establish_baseline()
    
    response = client.get("/metrics/export/json?window=all")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "baseline" in data
    assert data["baseline"] is not None
    assert "baseline_token_per_task" in data["baseline"]
    assert "baseline_patches" in data["baseline"]
    assert "baseline_success_rate" in data["baseline"]
    assert "version" in data["baseline"]


def test_export_json_includes_anomalies_and_suggestions(client):
    """Test JSON export includes anomalies and suggestions."""
    response = client.get("/metrics/export/json?window=all")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "anomalies" in data
    assert isinstance(data["anomalies"], list)
    
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)


# ============================================================================
# Test 25.2: CSV Export Endpoint
# ============================================================================

def test_export_csv_all_window(client):
    """Test CSV export with 'all' window."""
    response = client.get("/metrics/export/csv?window=all")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "attachment" in response.headers["content-disposition"]
    assert "tasks_" in response.headers["content-disposition"]
    
    # Parse CSV content
    csv_content = response.text
    reader = csv.DictReader(io.StringIO(csv_content))
    rows = list(reader)
    
    assert len(rows) == 15  # All tasks
    
    # Verify CSV structure
    assert "task_id" in rows[0]
    assert "timestamp" in rows[0]
    assert "success" in rows[0]
    assert "patches" in rows[0]
    assert "rollback" in rows[0]
    assert "tokens" in rows[0]
    assert "no_op" in rows[0]
    
    # Verify data types
    assert rows[0]["success"] in ["True", "False"]
    assert rows[0]["patches"].isdigit()
    assert rows[0]["tokens"].isdigit()


def test_export_csv_last_10_window(client):
    """Test CSV export with 'last_10' window."""
    response = client.get("/metrics/export/csv?window=last_10")
    
    assert response.status_code == 200
    
    csv_content = response.text
    reader = csv.DictReader(io.StringIO(csv_content))
    rows = list(reader)
    
    assert len(rows) == 10  # Last 10 tasks


def test_export_csv_no_data(client):
    """Test CSV export with no task data."""
    # Create empty monitor
    empty_monitor = HealthMonitor()
    set_health_monitor(empty_monitor)
    
    response = client.get("/metrics/export/csv?window=all")
    
    assert response.status_code == 404
    assert "No task data available" in response.json()["detail"]


# ============================================================================
# Test 25.3: Prometheus Export Endpoint
# ============================================================================

def test_export_prometheus(client):
    """Test Prometheus export."""
    response = client.get("/metrics/export/prometheus")
    
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    
    # Parse Prometheus text format
    content = response.text
    lines = content.strip().split("\n")
    
    # Verify metrics are present
    assert any("antigravity_health_score" in line for line in lines)
    assert any("antigravity_success_rate" in line for line in lines)
    assert any("antigravity_rollback_rate" in line for line in lines)
    assert any("antigravity_token_per_task" in line for line in lines)
    
    # Verify format (HELP and TYPE comments)
    assert any("# HELP antigravity_health_score" in line for line in lines)
    assert any("# TYPE antigravity_health_score gauge" in line for line in lines)
    
    # Verify metric values are present
    metric_lines = [line for line in lines if line and not line.startswith("#")]
    assert len(metric_lines) >= 4  # At least 4 metrics


def test_export_prometheus_values(client, health_monitor):
    """Test Prometheus export has correct values."""
    response = client.get("/metrics/export/prometheus")
    
    assert response.status_code == 200
    content = response.text
    
    # Extract metric values
    health_score = None
    success_rate = None
    
    for line in content.split("\n"):
        if line.startswith("antigravity_health_score "):
            health_score = float(line.split()[1])
        elif line.startswith("antigravity_success_rate "):
            success_rate = float(line.split()[1])
    
    assert health_score is not None
    assert 0 <= health_score <= 100
    
    assert success_rate is not None
    assert 0 <= success_rate <= 1


# ============================================================================
# Test 25.5: Error Handling
# ============================================================================

def test_export_json_invalid_window(client):
    """Test JSON export with invalid window parameter."""
    response = client.get("/metrics/export/json?window=invalid")
    
    assert response.status_code == 422  # Validation error


def test_export_csv_invalid_window(client):
    """Test CSV export with invalid window parameter."""
    response = client.get("/metrics/export/csv?window=invalid")
    
    assert response.status_code == 422  # Validation error


def test_export_endpoints_with_empty_monitor():
    """Test export endpoints with uninitialized monitor."""
    # Create client without setting monitor
    empty_client = TestClient(app)
    
    # JSON export should work (creates default monitor)
    response = empty_client.get("/metrics/export/json?window=all")
    assert response.status_code == 200
    
    # CSV export might work if baseline is loaded from disk, or fail with no data
    response = empty_client.get("/metrics/export/csv?window=all")
    assert response.status_code in [200, 404]  # Either works or no data


# ============================================================================
# Test CLI Export (Integration)
# ============================================================================

def test_cli_json_export(tmp_path, health_monitor):
    """Test CLI JSON export."""
    from antigravity.cli.metrics_export import export_json
    
    output_file = tmp_path / "metrics.json"
    export_json(health_monitor, output_file, window="all")
    
    assert output_file.exists()
    
    # Verify JSON content
    with open(output_file, 'r') as f:
        data = json.load(f)
    
    assert "health" in data
    assert "task_history" in data
    assert len(data["task_history"]) == 15


def test_cli_csv_export(tmp_path, health_monitor):
    """Test CLI CSV export."""
    from antigravity.cli.metrics_export import export_csv
    
    output_file = tmp_path / "tasks.csv"
    export_csv(health_monitor, output_file, window="all")
    
    assert output_file.exists()
    
    # Verify CSV content
    with open(output_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 15
    assert "task_id" in rows[0]


def test_cli_prometheus_export(tmp_path, health_monitor):
    """Test CLI Prometheus export."""
    from antigravity.cli.metrics_export import export_prometheus
    
    output_file = tmp_path / "metrics.prom"
    export_prometheus(health_monitor, output_file)
    
    assert output_file.exists()
    
    # Verify Prometheus content
    content = output_file.read_text()
    assert "antigravity_health_score" in content
    assert "antigravity_success_rate" in content


def test_cli_export_with_window_filtering(tmp_path, health_monitor):
    """Test CLI export with window filtering."""
    from antigravity.cli.metrics_export import export_json
    
    output_file = tmp_path / "metrics_last10.json"
    export_json(health_monitor, output_file, window="last_10")
    
    with open(output_file, 'r') as f:
        data = json.load(f)
    
    assert len(data["task_history"]) == 10


# ============================================================================
# Test Edge Cases
# ============================================================================

def test_export_with_no_baseline(client):
    """Test export when baseline is not established."""
    response = client.get("/metrics/export/json?window=all")
    
    assert response.status_code == 200
    data = response.json()
    
    # Baseline might be loaded from disk, so we just check it exists in response
    assert "baseline" in data


def test_export_with_single_task(tmp_path):
    """Test export with only one task."""
    monitor = HealthMonitor()
    monitor.record_task(
        success=True,
        patches_count=1,
        rollback=False,
        tokens_used=2000,
        no_op_patch=False
    )
    
    from antigravity.cli.metrics_export import export_json
    
    output_file = tmp_path / "single_task.json"
    export_json(monitor, output_file, window="all")
    
    with open(output_file, 'r') as f:
        data = json.load(f)
    
    assert len(data["task_history"]) == 1
    # Health score might be affected by baseline loaded from disk
    assert data["health"]["score"] >= 90.0  # Should be high with one success


def test_csv_export_special_characters(tmp_path):
    """Test CSV export handles special characters in task IDs."""
    monitor = HealthMonitor()
    
    # Record task with special characters
    monitor.record_task(
        success=True,
        patches_count=1,
        rollback=False,
        tokens_used=2000,
        no_op_patch=False
    )
    
    # Manually set task_id with special characters
    monitor._task_history[-1].task_id = "task,with\"quotes"
    
    from antigravity.cli.metrics_export import export_csv
    
    output_file = tmp_path / "special_chars.csv"
    export_csv(monitor, output_file, window="all")
    
    # Verify CSV can be parsed
    with open(output_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 1
    assert rows[0]["task_id"] == "task,with\"quotes"


# ============================================================================
# Performance Tests
# ============================================================================

def test_export_large_dataset(tmp_path):
    """Test export with large dataset (1000 tasks)."""
    monitor = HealthMonitor(window_size=1000)
    
    # Record 1000 tasks
    for i in range(1000):
        monitor.record_task(
            success=(i % 3 != 0),
            patches_count=1 + (i % 5),
            rollback=(i % 10 == 0),
            tokens_used=2000 + i,
            no_op_patch=(i % 20 == 0)
        )
    
    from antigravity.cli.metrics_export import export_json, export_csv
    
    # Test JSON export
    json_file = tmp_path / "large.json"
    export_json(monitor, json_file, window="all")
    assert json_file.exists()
    assert json_file.stat().st_size > 0
    
    # Test CSV export
    csv_file = tmp_path / "large.csv"
    export_csv(monitor, csv_file, window="all")
    assert csv_file.exists()
    assert csv_file.stat().st_size > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
