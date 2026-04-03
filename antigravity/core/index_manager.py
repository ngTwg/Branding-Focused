"""
IndexManager — Lifecycle management for skill embeddings.

Detects stale embeddings, triggers incremental reindex, and maintains index health.
Prevents silent degradation of retrieval quality.

Validates Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7
"""

from __future__ import annotations
import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from antigravity.core.hybrid_retriever import HybridRetriever

logger = logging.getLogger(__name__)


class IndexManager:
    """
    Manages skill index lifecycle with staleness detection and incremental reindex.
    
    Features:
    - SHA-256 checksums for change detection
    - Stale ratio tracking
    - Incremental and full reindex modes
    - Checkpoint/rollback support
    - Health metrics
    
    Validates Requirements:
    - 1.1: Detect file changes via checksums
    - 1.2: Track stale embeddings
    - 1.3: Compute stale ratio
    - 1.4: Incremental reindex
    - 1.5: Full reindex
    - 1.6: Integration with HybridRetriever
    - 1.7: Health metrics
    """

    def __init__(self, skills_dir: Path | str, cache_path: Path | str):
        """
        Initialize IndexManager.
        
        Args:
            skills_dir: Directory containing skill .md files
            cache_path: Directory for storing checksums and metadata
        """
        self.skills_dir = Path(skills_dir)
        self.cache_path = Path(cache_path)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        self.checksum_file = self.cache_path / "index_checksums.json"
        
        # Load existing checksums
        self._checksums: dict[str, str] = self._load_checksums()
        
        # Track stale files
        self._stale_files: set[str] = set()
        
        # Metadata
        self._last_index_time: datetime | None = None
        self._index_version: int = 0
        self._total_files: int = 0
        
        logger.info(f"IndexManager initialized: {len(self._checksums)} cached checksums")

    def _load_checksums(self) -> dict[str, str]:
        """Load checksums from cache file."""
        if not self.checksum_file.exists():
            return {}
        
        try:
            with open(self.checksum_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("checksums", {})
        except Exception as e:
            logger.warning(f"Failed to load checksums: {e}")
            return {}

    def _compute_checksum(self, file_path: Path) -> str:
        """Compute SHA-256 checksum for a file."""
        sha256 = hashlib.sha256()
        try:
            # Normalize line endings to avoid false-positive drift when files are
            # rewritten through text-mode IO on different platforms.
            content = file_path.read_text(encoding='utf-8')
            normalized = content.replace('\r\n', '\n').replace('\r', '\n')
            sha256.update(normalized.encode('utf-8'))
            return sha256.hexdigest()
        except Exception as e:
            try:
                with open(file_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(8192), b''):
                        sha256.update(chunk)
                return sha256.hexdigest()
            except Exception as fallback_err:
                logger.error(f"Failed to compute checksum for {file_path}: {fallback_err}")
                return ""

    def detect_changes(self) -> list[str]:
        """
        Detect changed skill files by comparing checksums.
        
        Returns:
            List of file paths that have changed
            
        Validates: Requirements 1.1, 1.2
        """
        changed_files = []
        
        # Scan all .md files in skills_dir
        skill_files = list(self.skills_dir.rglob("*.md"))
        self._total_files = len(skill_files)
        
        for file_path in skill_files:
            rel_path = str(file_path.relative_to(self.skills_dir))
            current_checksum = self._compute_checksum(file_path)
            
            if not current_checksum:
                continue
            
            cached_checksum = self._checksums.get(rel_path)
            
            if cached_checksum != current_checksum:
                changed_files.append(rel_path)
                logger.debug(f"Change detected: {rel_path}")
        
        # Check for deleted files
        for rel_path in list(self._checksums.keys()):
            full_path = self.skills_dir / rel_path
            if not full_path.exists():
                changed_files.append(rel_path)
                logger.debug(f"Deletion detected: {rel_path}")
        
        logger.info(f"Detected {len(changed_files)} changed files out of {self._total_files}")
        return changed_files

    def mark_stale(self, files: list[str]) -> None:
        """
        Mark files as stale (embeddings need update).
        
        Args:
            files: List of file paths to mark stale
            
        Validates: Requirements 1.2
        """
        self._stale_files.update(files)
        logger.info(f"Marked {len(files)} files as stale (total stale: {len(self._stale_files)})")

    def get_stale_ratio(self) -> float:
        """
        Compute ratio of stale files to total files.
        
        Returns:
            Stale ratio in [0.0, 1.0]
            
        Validates: Requirements 1.3
        """
        if self._total_files == 0:
            return 0.0
        
        return len(self._stale_files) / self._total_files

    def should_reindex(self, threshold: float = 0.2) -> bool:
        """
        Check if reindex is needed based on stale ratio.
        
        Args:
            threshold: Stale ratio threshold (default: 0.2 = 20%)
            
        Returns:
            True if stale_ratio > threshold
            
        Validates: Requirements 1.3
        """
        stale_ratio = self.get_stale_ratio()
        should_reindex = stale_ratio > threshold
        
        logger.info(
            f"Reindex check: stale_ratio={stale_ratio:.2%}, "
            f"threshold={threshold:.2%}, should_reindex={should_reindex}"
        )
        
        return should_reindex

    def reindex(
        self,
        retriever: HybridRetriever,
        mode: str = 'incremental'
    ) -> None:
        """
        Trigger reindex of skill embeddings.
        
        Args:
            retriever: HybridRetriever instance to reindex
            mode: 'incremental' (only stale files) or 'full' (all files)
            
        Validates: Requirements 1.4, 1.5, 1.6
        """
        if mode not in ('incremental', 'full'):
            raise ValueError(f"Invalid mode: {mode}. Must be 'incremental' or 'full'")
        
        logger.info(f"Starting {mode} reindex...")
        
        if mode == 'full':
            # Full reindex: all files
            files_to_index = list(self.skills_dir.rglob("*.md"))
            removed_files = [
                rel_path for rel_path in list(self._checksums.keys())
                if not (self.skills_dir / rel_path).exists()
            ]
            logger.info(f"Full reindex: {len(files_to_index)} files")
        else:
            # Incremental reindex: stale files only. Retriever may merge deltas
            # with existing in-memory corpus via apply_delta().
            removed_files = [
                rel_path for rel_path in self._stale_files
                if not (self.skills_dir / rel_path).exists()
            ]
            files_to_index = [
                self.skills_dir / rel_path
                for rel_path in self._stale_files
                if (self.skills_dir / rel_path).exists()
            ]
            logger.info(
                f"Incremental reindex: {len(files_to_index)} stale files, "
                f"{len(removed_files)} deleted files"
            )
        
        if not files_to_index:
            logger.info("No files to reindex")
            return
        
        # Load documents from files
        from antigravity.core.schemas import SkillDocument
        documents = []
        
        for file_path in files_to_index:
            try:
                content = file_path.read_text(encoding='utf-8')
                rel_path = str(file_path.relative_to(self.skills_dir))
                
                # Extract domain from path (e.g., "frontend/react.md" → "frontend")
                domain_tags = []
                parts = Path(rel_path).parts
                if len(parts) > 1:
                    domain_tags.append(parts[0])
                
                doc = SkillDocument(
                    skill_id=rel_path,
                    name=file_path.stem,
                    content=content,
                    domain_tags=domain_tags,
                    file_path=rel_path,
                )
                documents.append(doc)
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {e}")
        
        # Reindex via retriever
        try:
            supports_delta = callable(getattr(type(retriever), 'apply_delta', None))

            if mode == 'incremental' and supports_delta:
                retriever.apply_delta(documents, removed_ids=removed_files)
            else:
                retriever.index(documents)
            logger.info(f"Reindex complete: {len(documents)} documents indexed")
            
            # Update checksums
            for rel_path in removed_files:
                self._checksums.pop(rel_path, None)

            for file_path in files_to_index:
                rel_path = str(file_path.relative_to(self.skills_dir))
                checksum = self._compute_checksum(file_path)
                if checksum:
                    self._checksums[rel_path] = checksum
            
            # Clear stale files
            if mode == 'incremental':
                self._stale_files.clear()
            elif mode == 'full':
                # Full reindex clears all stale files
                self._stale_files.clear()
            
            # Update metadata
            self._last_index_time = datetime.now()
            self._index_version += 1
            
            # Save checksums
            self._save_checksums()
            
        except Exception as e:
            logger.error(f"Reindex failed: {e}", exc_info=True)
            raise

    def _save_checksums(self) -> None:
        """Save checksums to cache file."""
        data = {
            "checksums": self._checksums,
            "metadata": {
                "last_index_time": self._last_index_time.isoformat() if self._last_index_time else None,
                "index_version": self._index_version,
                "total_files": self._total_files,
            }
        }
        
        try:
            with open(self.checksum_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save checksums: {e}")

    def save_checkpoint(self, version: int) -> None:
        """
        Save index checkpoint for rollback.
        
        Args:
            version: Checkpoint version number
            
        Validates: Requirements 1.7
        """
        checkpoint_file = self.cache_path / f"index_checksums_v{version}.json"
        
        data = {
            "checksums": self._checksums.copy(),
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_files": self._total_files,
                "version": version,
            }
        }
        
        try:
            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Checkpoint saved: version {version}")
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")

    def rollback_index(self, version: int) -> None:
        """
        Rollback index to a previous checkpoint.
        
        Args:
            version: Checkpoint version to restore
            
        Validates: Requirements 1.7
        """
        checkpoint_file = self.cache_path / f"index_checksums_v{version}.json"
        
        if not checkpoint_file.exists():
            raise FileNotFoundError(f"Checkpoint version {version} not found")
        
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self._checksums = data["checksums"]
            # Don't update _total_files from checkpoint - it should reflect current state
            # self._total_files = data["metadata"]["total_files"]
            
            # Recompute stale files based on current files vs restored checksums
            self._stale_files.clear()
            changed = self.detect_changes()
            self.mark_stale(changed)
            
            logger.info(f"Rolled back to checkpoint version {version}")
            
        except Exception as e:
            logger.error(f"Rollback failed: {e}", exc_info=True)
            raise

    def get_health_metrics(self) -> dict:
        """
        Get index health metrics.
        
        Returns:
            Dictionary with health metrics
            
        Validates: Requirements 1.7
        """
        return {
            "total_skills": self._total_files,
            "stale_embeddings": len(self._stale_files),
            "last_index_time": self._last_index_time.isoformat() if self._last_index_time else None,
            "index_version": self._index_version,
            "stale_ratio": self.get_stale_ratio(),
        }
