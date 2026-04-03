"""
ErrorPrioritizer Core - Intelligent error prioritization and clustering.

This module implements Requirements 2.1 and 2.2:
- Sort errors by severity priority (SYNTAX > RUNTIME > LINT)
- Pick top-k errors to prevent LLM context overload
- Detect error dependency chains (root cause analysis)
- Estimate context size for budget management

**Validates: Requirements 2.1, 2.2**
"""

import re
from dataclasses import dataclass
from enum import IntEnum
from typing import Literal


class ErrorSeverity(IntEnum):
    """Error severity levels (lower number = higher priority)."""
    SYNTAX = 1      # Blocking errors (invalid syntax, parse errors)
    RUNTIME = 2     # Critical errors (exceptions, crashes)
    LINT = 3        # Minor warnings (style, unused variables)


@dataclass
class PrioritizedError:
    """
    Represents a prioritized error with metadata.
    
    Attributes:
        error_text: The full error message
        severity: ErrorSeverity level (SYNTAX/RUNTIME/LINT)
        line_number: Line number where error occurs (if available)
        file_path: File path where error occurs (if available)
        is_root_cause: Whether this is a root cause error
        dependent_errors: List of error texts that depend on this error
        context_tokens: Estimated token count for this error
    """
    error_text: str
    severity: ErrorSeverity
    line_number: int | None = None
    file_path: str | None = None
    is_root_cause: bool = False
    dependent_errors: list[str] | None = None
    context_tokens: int = 0


@dataclass
class ErrorCluster:
    """
    Represents a cluster of similar errors.
    
    Attributes:
        cluster_id: Unique identifier for the cluster
        error_type: Type of error (e.g., "NameError", "TypeError")
        affected_functions: List of function names affected
        error_count: Number of errors in this cluster
        representative_error: Example error from the cluster
        summary: Human-readable summary of the cluster
    """
    cluster_id: str
    error_type: str
    affected_functions: list[str]
    error_count: int
    representative_error: PrioritizedError
    summary: str


class ErrorPrioritizer:
    """
    Intelligent error prioritization and clustering.
    Prevents LLM context overload by focusing on root causes.
    
    **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6**
    """
    
    # Regex patterns for error classification
    SYNTAX_PATTERNS = [
        r"SyntaxError",
        r"invalid syntax",
        r"unexpected indent",
        r"unmatched ['\")\]]",
        r"expected [':']",
        r"IndentationError",
        r"ParseError",
        r"TabError",
        r"unexpected EOF",
    ]
    
    RUNTIME_PATTERNS = [
        r"RuntimeError",
        r"Exception",
        r"Traceback",
        r"NameError",
        r"TypeError",
        r"ValueError",
        r"AttributeError",
        r"KeyError",
        r"IndexError",
        r"ModuleNotFoundError",
        r"ImportError",
    ]
    
    LINT_PATTERNS = [
        r"^W\d{4}",  # Pylint warnings (start of line)
        r"^C\d{4}",  # Pylint conventions (start of line)
        r"^R\d{4}",  # Pylint refactoring (start of line)
        r"warning",
        r"unused variable",
        r"line too long",
        r"missing docstring",
        r"invalid-name",
        r"too-many",
    ]
    
    def _classify_error(self, error_text: str) -> ErrorSeverity:
        """
        Classify error and assign severity level.
        
        Args:
            error_text: The error message to classify
            
        Returns:
            ErrorSeverity level (SYNTAX/RUNTIME/LINT)
            
        **Validates: Requirement 2.1**
        """
        error_lower = error_text.lower()
        
        # Check lint patterns first (to catch W/C/R codes before they match other patterns)
        for pattern in self.LINT_PATTERNS:
            if re.search(pattern, error_text, re.IGNORECASE):
                return ErrorSeverity.LINT
        
        # Check syntax patterns (highest priority)
        for pattern in self.SYNTAX_PATTERNS:
            if re.search(pattern, error_text, re.IGNORECASE):
                return ErrorSeverity.SYNTAX
        
        # Check runtime patterns
        for pattern in self.RUNTIME_PATTERNS:
            if re.search(pattern, error_text, re.IGNORECASE):
                return ErrorSeverity.RUNTIME
        
        # Default to RUNTIME if unknown
        return ErrorSeverity.RUNTIME
    
    def estimate_context_size(self, error: PrioritizedError) -> int:
        """
        Estimate token count for an error.
        
        Uses heuristic: ~1.3 tokens per word + metadata overhead.
        
        Args:
            error: The PrioritizedError to estimate
            
        Returns:
            Estimated token count
        """
        # Count words in error text
        word_count = len(error.error_text.split())
        
        # Base tokens: ~1.3 tokens per word
        base_tokens = int(word_count * 1.3)
        
        # Add metadata overhead
        metadata_tokens = 50  # Base overhead for formatting
        
        # Add file path tokens
        if error.file_path:
            metadata_tokens += len(error.file_path.split()) * 1.3
        
        # Add line number tokens
        if error.line_number:
            metadata_tokens += 5
        
        # Add context tokens (surrounding code lines)
        context_tokens = 100  # Estimated context around error
        
        # Add dependent errors tokens
        if error.dependent_errors:
            for dep_error in error.dependent_errors:
                context_tokens += len(dep_error.split()) * 1.3
        
        return int(base_tokens + metadata_tokens + context_tokens)
    
    def prioritize_errors(
        self,
        errors: list[str],
        max_k: int = 3
    ) -> list[PrioritizedError]:
        """
        Sort errors by priority and return top-k.
        
        Priority order:
        1. SYNTAX errors (blocking)
        2. RUNTIME errors (critical)
        3. LINT warnings (minor)
        
        Within same severity, earlier errors are prioritized.
        
        Args:
            errors: List of error messages
            max_k: Maximum number of errors to return (default: 3)
            
        Returns:
            List of top-k PrioritizedError objects, sorted by priority
            
        **Validates: Requirements 2.1, 2.2**
        """
        if not errors:
            return []
        
        # Parse and classify all errors
        prioritized: list[PrioritizedError] = []
        
        for error_text in errors:
            # Extract file path and line number if present
            file_path = None
            line_number = None
            
            # Try to extract file:line pattern
            file_match = re.search(r'File "([^"]+)", line (\d+)', error_text)
            if file_match:
                file_path = file_match.group(1)
                line_number = int(file_match.group(2))
            else:
                # Try alternative pattern: path.py:123
                alt_match = re.search(r'(\S+\.py):(\d+)', error_text)
                if alt_match:
                    file_path = alt_match.group(1)
                    line_number = int(alt_match.group(2))
            
            # Classify error
            severity = self._classify_error(error_text)
            
            # Create prioritized error
            p_error = PrioritizedError(
                error_text=error_text,
                severity=severity,
                line_number=line_number,
                file_path=file_path,
                is_root_cause=False,  # Will be determined later
                dependent_errors=[]
            )
            
            # Estimate context size
            p_error.context_tokens = self.estimate_context_size(p_error)
            
            prioritized.append(p_error)
        
        # Sort by severity (lower number = higher priority), then by original order
        prioritized.sort(key=lambda e: (e.severity.value, errors.index(e.error_text)))
        
        # Return top-k errors
        return prioritized[:max_k]

    
    def detect_error_chains(
        self,
        errors: list[PrioritizedError]
    ) -> list[PrioritizedError]:
        """
        Detect error dependency chains and identify root causes.
        
        Logic:
        - SyntaxError in a file causes all other errors in that file
        - ImportError causes NameError for the imported name
        - Earlier errors in same file may cause later errors
        
        Args:
            errors: List of PrioritizedError objects
            
        Returns:
            List of root cause errors with dependent_errors populated
            
        **Validates: Requirements 2.3, 2.6**
        """
        if not errors:
            return []
        
        # Group errors by file
        errors_by_file: dict[str, list[PrioritizedError]] = {}
        for error in errors:
            file_path = error.file_path or "unknown"
            if file_path not in errors_by_file:
                errors_by_file[file_path] = []
            errors_by_file[file_path].append(error)
        
        root_causes: list[PrioritizedError] = []
        processed_errors: set[str] = set()
        
        for file_path, file_errors in errors_by_file.items():
            # Sort by line number (if available) and severity
            file_errors.sort(key=lambda e: (
                e.line_number if e.line_number else 999999,
                e.severity.value
            ))
            
            # Check for syntax errors (they block everything)
            syntax_errors = [e for e in file_errors if e.severity == ErrorSeverity.SYNTAX]
            if syntax_errors:
                # First syntax error is root cause
                root = syntax_errors[0]
                root.is_root_cause = True
                root.dependent_errors = [e.error_text for e in file_errors if e != root]
                root_causes.append(root)
                # Mark all errors in this file as processed
                for e in file_errors:
                    processed_errors.add(e.error_text)
                continue
            
            # Check for import errors causing name errors
            import_errors = [e for e in file_errors if "ImportError" in e.error_text or "ModuleNotFoundError" in e.error_text]
            name_errors = [e for e in file_errors if "NameError" in e.error_text and e.error_text not in processed_errors]
            
            if import_errors:
                # ImportError is always a root cause (it blocks imports)
                for imp_error in import_errors:
                    if imp_error.error_text in processed_errors:
                        continue
                    
                    imp_error.is_root_cause = True
                    
                    # Try to match import name with undefined names
                    import_match = re.search(r'No module named ["\'](\w+)["\']', imp_error.error_text)
                    if import_match:
                        module_name = import_match.group(1)
                        
                        # Find matching name errors
                        dependent = []
                        for name_error in name_errors:
                            # Check if the undefined name could be from the missing module
                            if name_error.error_text not in processed_errors:
                                dependent.append(name_error.error_text)
                                processed_errors.add(name_error.error_text)
                        
                        imp_error.dependent_errors = dependent
                    else:
                        # Generic import error - assume it affects subsequent name errors
                        imp_error.dependent_errors = [e.error_text for e in name_errors if e.error_text not in processed_errors]
                        for e in name_errors:
                            processed_errors.add(e.error_text)
                    
                    root_causes.append(imp_error)
                    processed_errors.add(imp_error.error_text)
            
            # Add remaining unprocessed errors as independent root causes
            for error in file_errors:
                if error.error_text not in processed_errors:
                    root_causes.append(error)
                    processed_errors.add(error.error_text)
        
        return root_causes
    
    def cluster_errors(
        self,
        errors: list[PrioritizedError]
    ) -> list[ErrorCluster]:
        """
        Group similar errors together.
        
        Clustering criteria:
        - Same error type (NameError, TypeError, etc.)
        - At least 2 errors of same type
        
        Args:
            errors: List of PrioritizedError objects
            
        Returns:
            List of ErrorCluster objects
            
        **Validates: Requirement 2.4**
        """
        if not errors:
            return []
        
        # Group by error type
        error_groups: dict[str, list[PrioritizedError]] = {}
        
        for error in errors:
            # Extract error type (e.g., "NameError", "TypeError")
            error_type = "Unknown"
            for pattern in ["NameError", "TypeError", "ValueError", "AttributeError", 
                          "KeyError", "IndexError", "ImportError", "SyntaxError"]:
                if pattern in error.error_text:
                    error_type = pattern
                    break
            
            if error_type not in error_groups:
                error_groups[error_type] = []
            error_groups[error_type].append(error)
        
        # Create clusters (only for groups with 2+ errors)
        clusters: list[ErrorCluster] = []
        
        for error_type, group_errors in error_groups.items():
            if len(group_errors) < 2:
                continue
            
            # Extract affected functions
            affected_functions = []
            for error in group_errors:
                # Try to extract function name from error message
                func_match = re.search(r'in (\w+)', error.error_text)
                if func_match:
                    func_name = func_match.group(1)
                    if func_name not in affected_functions:
                        affected_functions.append(func_name)
            
            # Create cluster
            cluster = ErrorCluster(
                cluster_id=f"{error_type}_{len(clusters)}",
                error_type=error_type,
                affected_functions=affected_functions,
                error_count=len(group_errors),
                representative_error=group_errors[0],
                summary=f"{len(group_errors)}x {error_type}" + 
                       (f" in {', '.join(affected_functions)}" if affected_functions else "")
            )
            clusters.append(cluster)
        
        return clusters
    
    def format_clusters_for_llm(
        self,
        clusters: list[ErrorCluster]
    ) -> str:
        """
        Format error clusters for LLM prompt.
        
        Args:
            clusters: List of ErrorCluster objects
            
        Returns:
            Formatted string for LLM prompt
            
        **Validates: Requirements 2.4, 2.5**
        """
        if not clusters:
            return ""
        
        lines = ["[ERROR CLUSTERS]"]
        lines.append("Multiple similar errors detected:\n")
        
        for cluster in clusters:
            lines.append(f"• {cluster.summary}")
            lines.append(f"  Representative: {cluster.representative_error.error_text[:100]}...")
            lines.append("")
        
        return "\n".join(lines)
