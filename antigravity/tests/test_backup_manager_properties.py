"""
Property-based tests for BackupManager.

Feature: antigravity-architecture-upgrade
Validates: Requirements 3.3, 3.7, 3.8
"""

import hashlib
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from antigravity.core.backup_manager import BackupManager
from antigravity.core.id_utils import new_id


class TestBackupManagerProperties:
    """Property tests for BackupManager rollback and idempotence."""

    @given(
        file_content=st.text(min_size=1, max_size=1000),
        patch_content=st.text(min_size=1, max_size=1000),
    )
    @settings(max_examples=100)
    def test_rollback_round_trip_invariant(self, file_content, patch_content):
        """
        Property 10: Rollback Round-Trip Invariant.
        
        Validates: Requirements 3.3, 3.8
        
        After backup → modify → rollback, file content must match original SHA-256 hash.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text(file_content, encoding="utf-8")
            original_hash = hashlib.sha256(file_content.encode("utf-8")).hexdigest()

            session_id = new_id()
            operation_id = new_id()
            backup_mgr = BackupManager(backup_root=Path(tmpdir) / "backups")

            # Backup
            backup_mgr.create_backup(session_id, operation_id, [str(test_file)])

            # Modify
            test_file.write_text(patch_content, encoding="utf-8")

            # Rollback
            backup_mgr.rollback(session_id, operation_id)

            # Verify
            restored_content = test_file.read_text(encoding="utf-8")
            restored_hash = hashlib.sha256(restored_content.encode("utf-8")).hexdigest()

            assert restored_hash == original_hash, (
                f"Rollback failed: hash mismatch\n"
                f"Expected: {original_hash}\n"
                f"Got: {restored_hash}"
            )

    @given(
        n_backups=st.integers(min_value=2, max_value=10),
        file_paths=st.lists(
            st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"))),
            min_size=1,
            max_size=5,
            unique=True,
        ),
    )
    @settings(max_examples=50)
    def test_backup_idempotence(self, n_backups, file_paths):
        """
        Property 11: Backup Idempotence.
        
        Validates: Requirements 3.7
        
        Multiple backups with same operation_id should not duplicate files.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup
            test_files = []
            for fname in file_paths:
                fpath = Path(tmpdir) / f"{fname}.txt"
                fpath.write_text(f"content_{fname}", encoding="utf-8")
                test_files.append(str(fpath))

            session_id = new_id()
            operation_id = new_id()
            backup_mgr = BackupManager(backup_root=Path(tmpdir) / "backups")

            # Backup n times with same operation_id
            for _ in range(n_backups):
                backup_mgr.create_backup(session_id, operation_id, test_files)

            # Count backup files
            backup_dir = backup_mgr._backup_path(session_id, operation_id)
            backup_files = list(backup_dir.rglob("*.txt"))

            # Assert: should have exactly len(unique_file_paths) files
            assert len(backup_files) == len(file_paths), (
                f"Backup idempotence violated: expected {len(file_paths)} files, got {len(backup_files)}"
            )
