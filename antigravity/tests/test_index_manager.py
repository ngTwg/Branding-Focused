"""
Unit and Integration Tests for IndexManager

Tests index lifecycle management: change detection, stale tracking,
incremental/full reindex, checkpoints, and health metrics.

Requirements: 1.1-1.7 from antigravity-resilience-upgrade spec.
"""

import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, MagicMock

import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

from antigravity.core.index_manager import IndexManager
from antigravity.core.schemas import SkillDocument


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def temp_skills_dir():
    """Create temporary skills directory with sample files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        skills_dir = Path(tmpdir) / "skills"
        skills_dir.mkdir()
        
        # Create sample skill files
        (skills_dir / "skill1.md").write_text("# Skill 1\nContent for skill 1", encoding='utf-8')
        (skills_dir / "skill2.md").write_text("# Skill 2\nContent for skill 2", encoding='utf-8')
        (skills_dir / "skill3.md").write_text("# Skill 3\nContent for skill 3", encoding='utf-8')
        
        yield skills_dir


@pytest.fixture
def temp_cache_dir():
    """Create temporary cache directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def index_manager(temp_skills_dir, temp_cache_dir):
    """Create IndexManager instance with temp directories."""
    return IndexManager(
        skills_dir=temp_skills_dir,
        cache_path=temp_cache_dir
    )


# ── Unit Tests: Change Detection ──────────────────────────────────────────────

def test_detect_changes_initial_scan(index_manager, temp_skills_dir):
    """
    Test initial scan detects all files as changed.
    
    Requirements: 1.1
    """
    changed = index_manager.detect_changes()
    
    # All files should be detected as changed (no cached checksums)
    assert len(changed) == 3
    assert "skill1.md" in changed
    assert "skill2.md" in changed
    assert "skill3.md" in changed


def test_detect_changes_after_modification(index_manager, temp_skills_dir):
    """
    Test detect_changes() identifies modified files.
    
    Requirements: 1.1
    """
    # Initial scan
    changed = index_manager.detect_changes()
    index_manager.mark_stale(changed)
    
    # Update checksums (simulate successful index)
    for file_path in temp_skills_dir.rglob("*.md"):
        rel_path = str(file_path.relative_to(temp_skills_dir))
        checksum = index_manager._compute_checksum(file_path)
        index_manager._checksums[rel_path] = checksum
    
    # Clear stale files
    index_manager._stale_files.clear()
    
    # Modify one file
    skill1_path = temp_skills_dir / "skill1.md"
    skill1_path.write_text("# Skill 1\nMODIFIED CONTENT", encoding='utf-8')
    
    # Detect changes again
    changed = index_manager.detect_changes()
    
    # Only modified file should be detected
    assert len(changed) == 1
    assert "skill1.md" in changed


def test_detect_changes_file_deletion(index_manager, temp_skills_dir):
    """
    Test detect_changes() identifies deleted files.
    
    Requirements: 1.1
    """
    # Initial scan and cache checksums
    changed = index_manager.detect_changes()
    for file_path in temp_skills_dir.rglob("*.md"):
        rel_path = str(file_path.relative_to(temp_skills_dir))
        checksum = index_manager._compute_checksum(file_path)
        index_manager._checksums[rel_path] = checksum
    
    # Delete one file
    (temp_skills_dir / "skill2.md").unlink()
    
    # Detect changes
    changed = index_manager.detect_changes()
    
    # Deleted file should be detected
    assert "skill2.md" in changed


# ── Unit Tests: Stale Tracking ────────────────────────────────────────────────

def test_stale_ratio_calculation(index_manager):
    """
    Test get_stale_ratio() computes correct ratio.
    
    Requirements: 1.2, 1.3
    """
    # Initial state: no stale files
    index_manager._total_files = 10
    index_manager._stale_files = set()
    
    assert index_manager.get_stale_ratio() == 0.0
    
    # Mark 2 files stale
    index_manager.mark_stale(["skill1.md", "skill2.md"])
    
    assert index_manager.get_stale_ratio() == 0.2  # 2/10 = 0.2
    
    # Mark 3 more files stale
    index_manager.mark_stale(["skill3.md", "skill4.md", "skill5.md"])
    
    assert index_manager.get_stale_ratio() == 0.5  # 5/10 = 0.5


def test_stale_ratio_edge_case_zero_files(index_manager):
    """
    Test get_stale_ratio() handles zero files gracefully.
    
    Requirements: 1.3
    """
    index_manager._total_files = 0
    index_manager._stale_files = set()
    
    # Should return 0.0, not raise ZeroDivisionError
    assert index_manager.get_stale_ratio() == 0.0


def test_should_reindex_threshold(index_manager):
    """
    Test should_reindex() respects threshold.
    
    Requirements: 1.3
    """
    index_manager._total_files = 10
    
    # 1/10 = 10% stale (below 20% threshold)
    index_manager._stale_files = {"skill1.md"}
    assert not index_manager.should_reindex(threshold=0.2)
    
    # 3/10 = 30% stale (above 20% threshold)
    index_manager._stale_files = {"skill1.md", "skill2.md", "skill3.md"}
    assert index_manager.should_reindex(threshold=0.2)


# ── Unit Tests: Incremental Reindex ───────────────────────────────────────────

def test_incremental_reindex(index_manager, temp_skills_dir):
    """
    Test incremental reindex only processes stale files.
    
    Requirements: 1.4
    """
    # Setup: mark 2 files as stale
    index_manager._total_files = 3
    index_manager.mark_stale(["skill1.md", "skill2.md"])
    
    # Mock retriever
    mock_retriever = Mock()
    mock_retriever.index = Mock()
    
    # Perform incremental reindex
    index_manager.reindex(mock_retriever, mode='incremental')
    
    # Verify only 2 documents indexed
    mock_retriever.index.assert_called_once()
    indexed_docs = mock_retriever.index.call_args[0][0]
    assert len(indexed_docs) == 2
    
    # Verify stale files cleared
    assert len(index_manager._stale_files) == 0
    
    # Verify metadata updated
    assert index_manager._last_index_time is not None
    assert index_manager._index_version == 1


def test_full_reindex(index_manager, temp_skills_dir):
    """
    Test full reindex processes all files.
    
    Requirements: 1.5
    """
    # Setup: mark 1 file as stale
    index_manager._total_files = 3
    index_manager.mark_stale(["skill1.md"])
    
    # Mock retriever
    mock_retriever = Mock()
    mock_retriever.index = Mock()
    
    # Perform full reindex
    index_manager.reindex(mock_retriever, mode='full')
    
    # Verify all 3 documents indexed
    mock_retriever.index.assert_called_once()
    indexed_docs = mock_retriever.index.call_args[0][0]
    assert len(indexed_docs) == 3


def test_reindex_invalid_mode(index_manager):
    """Test reindex() rejects invalid mode."""
    mock_retriever = Mock()
    
    with pytest.raises(ValueError, match="Invalid mode"):
        index_manager.reindex(mock_retriever, mode='invalid')


# ── Unit Tests: Checkpoints & Rollback ────────────────────────────────────────

def test_save_checkpoint(index_manager, temp_cache_dir):
    """
    Test save_checkpoint() persists checksums.
    
    Requirements: 1.7
    """
    # Setup checksums
    index_manager._checksums = {
        "skill1.md": "abc123",
        "skill2.md": "def456"
    }
    index_manager._total_files = 2
    
    # Save checkpoint
    index_manager.save_checkpoint(version=1)
    
    # Verify checkpoint file created
    checkpoint_file = temp_cache_dir / "index_checksums_v1.json"
    assert checkpoint_file.exists()
    
    # Verify content
    with open(checkpoint_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    assert data["checksums"] == index_manager._checksums
    assert data["metadata"]["version"] == 1
    assert data["metadata"]["total_files"] == 2


def test_rollback_index(index_manager, temp_cache_dir):
    """
    Test rollback_index() restores previous state.
    
    Requirements: 1.7
    """
    # Setup initial state
    index_manager._checksums = {
        "skill1.md": "abc123",
        "skill2.md": "def456"
    }
    index_manager._total_files = 2
    
    # Save checkpoint
    index_manager.save_checkpoint(version=1)
    
    # Modify state
    index_manager._checksums["skill3.md"] = "ghi789"
    index_manager._total_files = 3
    
    # Rollback
    index_manager.rollback_index(version=1)
    
    # Verify state restored
    assert len(index_manager._checksums) == 2
    assert "skill3.md" not in index_manager._checksums
    # _total_files should reflect current state (3 files exist), not checkpoint state
    assert index_manager._total_files == 3


def test_rollback_nonexistent_checkpoint(index_manager):
    """Test rollback_index() raises error for missing checkpoint."""
    with pytest.raises(FileNotFoundError, match="Checkpoint version 99 not found"):
        index_manager.rollback_index(version=99)


# ── Unit Tests: Health Metrics ─────────────────────────────────────────────────

def test_get_health_metrics(index_manager):
    """
    Test get_health_metrics() returns correct data.
    
    Requirements: 1.7
    """
    # Setup state
    index_manager._total_files = 10
    index_manager._stale_files = {"skill1.md", "skill2.md"}
    index_manager._last_index_time = datetime(2026, 3, 30, 10, 0, 0)
    index_manager._index_version = 5
    
    # Get metrics
    metrics = index_manager.get_health_metrics()
    
    # Verify
    assert metrics["total_skills"] == 10
    assert metrics["stale_embeddings"] == 2
    assert metrics["stale_ratio"] == 0.2
    assert metrics["index_version"] == 5
    assert metrics["last_index_time"] == "2026-03-30T10:00:00"


# ── Integration Test: Full Lifecycle ──────────────────────────────────────────

def test_full_lifecycle(temp_skills_dir, temp_cache_dir):
    """
    Integration test: full index lifecycle.
    
    Validates: Requirements 1.1-1.7
    """
    # Step 1: Initial index
    manager = IndexManager(temp_skills_dir, temp_cache_dir)
    
    changed = manager.detect_changes()
    assert len(changed) == 3
    
    manager.mark_stale(changed)
    assert manager.get_stale_ratio() == 1.0  # All files stale
    
    # Mock retriever and perform initial index
    mock_retriever = Mock()
    mock_retriever.index = Mock()
    
    manager.reindex(mock_retriever, mode='full')
    
    assert manager._index_version == 1
    assert len(manager._stale_files) == 0
    
    # Step 2: Modify one file
    skill1_path = temp_skills_dir / "skill1.md"
    skill1_path.write_text("# Skill 1\nMODIFIED", encoding='utf-8')
    
    changed = manager.detect_changes()
    assert len(changed) == 1
    assert "skill1.md" in changed
    
    manager.mark_stale(changed)
    assert manager.get_stale_ratio() == pytest.approx(0.333, abs=0.01)
    
    # Step 3: Incremental reindex
    manager.reindex(mock_retriever, mode='incremental')
    
    assert manager._index_version == 2
    assert len(manager._stale_files) == 0
    
    # Step 4: Save checkpoint
    manager.save_checkpoint(version=2)
    
    checkpoint_file = temp_cache_dir / "index_checksums_v2.json"
    assert checkpoint_file.exists()
    
    # Step 5: Verify health metrics
    metrics = manager.get_health_metrics()
    assert metrics["total_skills"] == 3
    assert metrics["stale_embeddings"] == 0
    assert metrics["stale_ratio"] == 0.0
    assert metrics["index_version"] == 2


# ── Property Tests: Checksum Stability ────────────────────────────────────────

@given(content=st.text(min_size=0, max_size=1000))
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_checksum_deterministic(content, temp_skills_dir, temp_cache_dir):
    """
    Property test: SHA-256 checksums are deterministic.
    
    Same content → same checksum.
    
    Requirements: 1.1
    """
    manager = IndexManager(temp_skills_dir, temp_cache_dir)
    
    # Write content to file
    test_file = temp_skills_dir / "test.md"
    test_file.write_text(content, encoding='utf-8')
    
    # Compute checksum twice
    checksum1 = manager._compute_checksum(test_file)
    checksum2 = manager._compute_checksum(test_file)
    
    # Should be identical
    assert checksum1 == checksum2
    assert len(checksum1) == 64  # SHA-256 hex digest length


@given(content1=st.text(min_size=1, max_size=100), content2=st.text(min_size=1, max_size=100))
@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_checksum_uniqueness(content1, content2, temp_skills_dir, temp_cache_dir):
    """
    Property test: Different content → different checksums (with high probability).
    
    Requirements: 1.1
    """
    # Skip if contents are identical
    if content1 == content2:
        return
    
    manager = IndexManager(temp_skills_dir, temp_cache_dir)
    
    # Write different contents
    file1 = temp_skills_dir / "file1.md"
    file2 = temp_skills_dir / "file2.md"
    
    file1.write_text(content1, encoding='utf-8')
    file2.write_text(content2, encoding='utf-8')
    
    # Compute checksums
    checksum1 = manager._compute_checksum(file1)
    checksum2 = manager._compute_checksum(file2)
    
    # Should be different (collision probability negligible)
    assert checksum1 != checksum2


@given(content=st.text(min_size=0, max_size=1000))
@settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_unchanged_file_unchanged_checksum(content, temp_skills_dir, temp_cache_dir):
    """
    Property test: Unchanged file → unchanged checksum.
    
    Requirements: 1.1
    """
    manager = IndexManager(temp_skills_dir, temp_cache_dir)
    
    # Write content
    test_file = temp_skills_dir / "test.md"
    test_file.write_text(content, encoding='utf-8')
    
    # Initial checksum
    checksum_before = manager._compute_checksum(test_file)
    
    # Read and write same content (no actual change)
    existing_content = test_file.read_text(encoding='utf-8')
    test_file.write_text(existing_content, encoding='utf-8')
    
    # Checksum after
    checksum_after = manager._compute_checksum(test_file)
    
    # Should be unchanged
    assert checksum_before == checksum_after
