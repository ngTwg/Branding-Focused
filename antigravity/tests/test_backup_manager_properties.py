"""
Property-based tests for BackupManager.

Feature: antigravity-architecture-upgrade
Tests backup/rollback invariants using Hypothesis.
"""

import hashlib
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from core.backup_manager import BackupManager
from core.id_utils import new_id


# Feature: antigravity-architecture-upgrade, Property 10: Rollback Round-Trip Invariant
@given(
    file_content=st.text(min_size=1, max_size=1000),
    patch_content=st.text(min_size=1, max_size=1000),
)
@settings(max_examples=50)
def test_rollback_round_trip_invariant(file_content, patch_content):
    """
    Property 10: Rollback Round-Trip Invariant
    Validates: Requirements 3.3, 3.8
    
    Verify that backup → modify → rollback restores original content exactly.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup
        test_file = Path(tmpdir) / "test_file.py"
        test_file.write_text(file_content, encoding="utf-8", newline='')
        # Read back to get actual stored content (handles line ending normalization)
        actual_content = test_file.read_text(encoding="utf-8")
        original_hash = hashlib.sha256(actual_content.encode("utf-8")).hexdigest()
        
        session_id = new_id()
        operation_id = new_id()
        backup_manager = BackupManager(backup_root=Path(tmpdir) / "backups")
        
        # Step 1: Create backup
        backup_manager.create_backup(
            session_id=session_id,
            operation_id=operation_id,
            file_paths=[str(test_file)]
        )
        
        # Step 2: Modify file (apply patch)
        test_file.write_text(patch_content, encoding="utf-8")
        
        # Step 3: Rollback
        backup_manager.rollback(session_id=session_id, operation_id=operation_id)
        
        # Step 4: Verify restoration
        restored_content = test_file.read_text(encoding="utf-8")
        restored_hash = hashlib.sha256(restored_content.encode("utf-8")).hexdigest()
        
        # Assert: Content restored exactly
        assert restored_hash == original_hash, (
            f"Rollback failed to restore original content.\n"
            f"Original hash: {original_hash}\n"
            f"Restored hash: {restored_hash}"
        )


# Feature: antigravity-architecture-upgrade, Property 11: Backup Idempotence
@given(
    n_backups=st.integers(min_value=2, max_value=10),
    file_paths=st.lists(
        st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"))),
        min_size=1,
        max_size=5,
        unique=True
    ),
)
@settings(max_examples=50)
def test_backup_idempotence(n_backups, file_paths):
    """
    Property 11: Backup Idempotence
    Validates: Requirements 3.7
    
    Verify that multiple backups with same operation_id are idempotent.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup: Create test files
        test_files = []
        for i, name in enumerate(file_paths):
            test_file = Path(tmpdir) / f"{name}_{i}.py"
            test_file.write_text(f"content_{i}", encoding="utf-8")
            test_files.append(str(test_file))
        
        session_id = new_id()
        operation_id = new_id()
        backup_manager = BackupManager(backup_root=Path(tmpdir) / "backups")
        
        # Step 1: Call create_backup() n times with same operation_id
        for _ in range(n_backups):
            backup_manager.create_backup(
                session_id=session_id,
                operation_id=operation_id,
                file_paths=test_files
            )
        
        # Step 2: Count backup files
        backup_dir = backup_manager._backup_path(session_id, operation_id)
        backup_files = list(backup_dir.glob("**/*"))
        backup_files = [f for f in backup_files if f.is_file()]
        
        # Assert: Number of backup files == number of unique source files
        assert len(backup_files) == len(test_files), (
            f"Backup not idempotent: expected {len(test_files)} files, "
            f"got {len(backup_files)} files after {n_backups} backup calls"
        )
