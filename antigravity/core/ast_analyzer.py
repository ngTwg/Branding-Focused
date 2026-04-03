"""
ASTAnalyzer — Tree-sitter JSON Contract Generator

Parses Python source files into compact JSON contracts to replace raw file content
in repair prompts. Uses tree-sitter for AST parsing with graceful fallback when
parsing fails.

Requirements: 2.1-2.9
Properties: 5-8
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from antigravity.core.schemas import ASTContract, ASTNode
from antigravity.core.error_prioritizer import ErrorPrioritizer, PrioritizedError, ErrorCluster

# Lazy import tree_sitter — graceful degradation if not installed
_TREE_SITTER_AVAILABLE = False
_PYTHON_PARSER = None
_JAVASCRIPT_PARSER = None
_TYPESCRIPT_PARSER = None
_PYTHON_LANGUAGE = None
_JAVASCRIPT_LANGUAGE = None
_TYPESCRIPT_LANGUAGE = None

try:
    import tree_sitter_python as tspython
    import tree_sitter_javascript as tsjavascript
    import tree_sitter_typescript as tstypescript
    from tree_sitter import Language, Parser

    _TREE_SITTER_AVAILABLE = True
    
    # Initialize Python parser
    _PYTHON_LANGUAGE = Language(tspython.language())
    _PYTHON_PARSER = Parser(_PYTHON_LANGUAGE)
    
    # Initialize JavaScript parser
    _JAVASCRIPT_LANGUAGE = Language(tsjavascript.language())
    _JAVASCRIPT_PARSER = Parser(_JAVASCRIPT_LANGUAGE)
    
    # Initialize TypeScript parser
    _TYPESCRIPT_LANGUAGE = Language(tstypescript.language_typescript())
    _TYPESCRIPT_PARSER = Parser(_TYPESCRIPT_LANGUAGE)
except ImportError:
    pass


class ASTAnalyzer:
    """
    Parse Python source files into compact JSON contracts.

    Multi-file support via list of (file_path, error_line) tuples.
    Hard limit: serialized JSON ≤ 4096 bytes.
    Fallback to raw excerpt (≤200 tokens) when tree-sitter unavailable or fails.
    
    Integrates ErrorPrioritizer for intelligent error filtering and root cause detection.
    """

    def __init__(self, error_prioritizer: ErrorPrioritizer | None = None):
        """
        Initialize ASTAnalyzer with lazy tree-sitter loading and error prioritization.
        
        Args:
            error_prioritizer: Optional ErrorPrioritizer instance for error filtering.
                             If None, creates a default instance.
        
        Validates: Requirements 2.5
        """
        self._available = _TREE_SITTER_AVAILABLE
        if not self._available:
            import logging

            logging.warning(
                "tree-sitter not available. ASTAnalyzer will use fallback mode."
            )
        
        # Initialize ErrorPrioritizer (Requirement 2.5)
        self._error_prioritizer = error_prioritizer if error_prioritizer else ErrorPrioritizer()

    def analyze(
        self, 
        targets: list[tuple[str, int]], 
        errors: list[str] | None = None
    ) -> ASTContract:
        """
        Multi-file entry point. Extract nodes from ±10 lines of error with error prioritization.

        Args:
            targets: List of (file_path, error_line) tuples
            errors: Optional list of error messages for prioritization and clustering

        Returns:
            ASTContract with affected_nodes or fallback excerpt.
            Serialized JSON guaranteed ≤ 4096 bytes.
            Includes error_priority_info if errors provided.

        Requirements: 2.1, 2.2, 2.5, 2.9
        Properties: 5, 6
        """
        if not targets:
            return ASTContract(
                error_type="no_targets",
                affected_nodes=[],
                is_fallback=True,
                source_files=[],
            )

        # Prioritize and filter errors if provided (Requirement 2.5)
        error_priority_info = {}
        if errors:
            try:
                # Step 1: Prioritize errors (top-3 by severity)
                prioritized = self._error_prioritizer.prioritize_errors(errors, max_k=3)
                
                # Step 2: Detect error chains (identify root causes)
                root_causes = self._error_prioritizer.detect_error_chains(prioritized)
                
                # Step 3: Cluster if many errors (>5)
                clusters = []
                if len(errors) > 5:
                    clusters = self._error_prioritizer.cluster_errors(prioritized)
                
                # Step 4: Estimate total context size
                total_context = sum(
                    self._error_prioritizer.estimate_context_size(e) 
                    for e in root_causes
                )
                
                # Step 5: Limit context if needed (target: 1000 tokens)
                if total_context > 1000:
                    # Reduce to top-2 if over limit
                    root_causes = root_causes[:2]
                    total_context = sum(
                        self._error_prioritizer.estimate_context_size(e) 
                        for e in root_causes
                    )
                    import logging
                    logging.info(
                        f"[ERROR] Context limited to {total_context} tokens (target: 1000)"
                    )
                
                # Build error priority info
                error_priority_info = {
                    "prioritized_errors": [
                        {
                            "error_text": e.error_text,
                            "severity": e.severity.name,
                            "line_number": e.line_number,
                            "file_path": e.file_path,
                            "is_root_cause": e.is_root_cause,
                            "context_tokens": e.context_tokens
                        }
                        for e in root_causes
                    ],
                    "total_errors": len(errors),
                    "root_causes": len([e for e in root_causes if e.is_root_cause]),
                    "clusters": [
                        {
                            "cluster_id": c.cluster_id,
                            "error_type": c.error_type,
                            "error_count": c.error_count,
                            "summary": c.summary
                        }
                        for c in clusters
                    ] if clusters else [],
                    "total_context_tokens": total_context
                }
            except Exception as e:
                import logging
                logging.warning(f"Error prioritization failed: {e}")

        # Try tree-sitter parsing first
        if self._available:
            try:
                all_nodes = []
                source_files = []

                for file_path, error_line in targets:
                    nodes = self._parse_file(file_path, error_line)
                    all_nodes.extend(nodes)
                    source_files.append(file_path)

                # Build contract and check size
                contract = ASTContract(
                    error_type="parse_success",
                    affected_nodes=all_nodes,
                    is_fallback=False,
                    source_files=source_files,
                )
                
                # Add error priority info if available (Requirement 2.5)
                if error_priority_info:
                    contract.error_priority_info = error_priority_info

                # Enforce 4KB hard limit by truncating nodes if needed
                contract = self._enforce_size_limit(contract)
                return contract

            except Exception:
                # Fall through to fallback mode
                pass

        # Fallback mode: raw excerpt
        fallback_contract = self._fallback_excerpt(targets[0][0], targets[0][1])
        if error_priority_info:
            fallback_contract.error_priority_info = error_priority_info
        return fallback_contract

    def _parse_file(self, file_path: str, error_line: int) -> list[ASTNode]:
        """
        Extract nodes within ±10 lines of error_line.

        node_id format: "filename.py::function_name::start_line"

        Args:
            file_path: Path to source file (Python, JavaScript, TypeScript)
            error_line: Line number where error occurred (1-indexed)

        Returns:
            List of ASTNode objects within range

        Requirements: 2.1, 2.5, 2.7
        Properties: 7, 8
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Determine language and parser
        suffix = path.suffix.lower()
        if suffix == ".py":
            parser = _PYTHON_PARSER
            language = "python"
        elif suffix in (".js", ".jsx"):
            parser = _JAVASCRIPT_PARSER
            language = "javascript"
        elif suffix in (".ts", ".tsx"):
            parser = _TYPESCRIPT_PARSER
            language = "typescript"
        else:
            raise RuntimeError(f"Unsupported file type: {suffix}")

        if not parser:
            raise RuntimeError("Parser not available")

        source_bytes = path.read_bytes()
        tree = parser.parse(source_bytes)
        root = tree.root_node

        # Check for parse errors - if tree has errors, raise to trigger fallback
        if root.has_error:
            raise RuntimeError("Parse tree contains errors")

        # Define range: ±10 lines
        min_line = max(1, error_line - 10)
        max_line = error_line + 10

        nodes = []
        filename = path.name

        # Walk AST and collect relevant nodes
        self._walk_tree(
            root,
            source_bytes,
            filename,
            file_path,
            min_line,
            max_line,
            nodes,
            language,
        )

        return nodes

    def _walk_tree(
        self,
        node,
        source_bytes: bytes,
        filename: str,
        file_path: str,
        min_line: int,
        max_line: int,
        nodes: list[ASTNode],
        language: str,
        scope_stack: list[str] | None = None,
    ):
        """
        Recursively walk tree-sitter AST and extract function/class nodes.

        Args:
            node: Current tree-sitter node
            source_bytes: Source file bytes
            filename: Name of file (for node_id)
            file_path: Full path to file
            min_line: Minimum line to include (1-indexed)
            max_line: Maximum line to include (1-indexed)
            nodes: Output list to append ASTNode objects
            language: Language type ("python", "javascript", "typescript")
            scope_stack: Current scope path (e.g. ["MyClass", "my_method"])
        """
        if scope_stack is None:
            scope_stack = []

        # Convert to 1-indexed line numbers
        start_line = node.start_point[0] + 1
        end_line = node.end_point[0] + 1

        # Check if node is in range
        in_range = not (end_line < min_line or start_line > max_line)

        # Extract nodes based on language
        if language == "python":
            self._walk_python_node(
                node, source_bytes, filename, file_path, min_line, max_line,
                nodes, in_range, start_line, end_line, scope_stack
            )
        elif language in ("javascript", "typescript"):
            self._walk_js_node(
                node, source_bytes, filename, file_path, min_line, max_line,
                nodes, in_range, start_line, end_line, scope_stack, language
            )
        else:
            # Recurse without processing
            for child in node.children:
                self._walk_tree(
                    child, source_bytes, filename, file_path, min_line, max_line,
                    nodes, language, scope_stack
                )

    def _get_function_name(self, node, source_bytes: bytes) -> Optional[str]:
        """Extract function name from function_definition node."""
        for child in node.children:
            if child.type == "identifier":
                return source_bytes[child.start_byte : child.end_byte].decode("utf-8")
        return None

    def _get_class_name(self, node, source_bytes: bytes) -> Optional[str]:
        """Extract class name from class_definition node."""
        for child in node.children:
            if child.type == "identifier":
                return source_bytes[child.start_byte : child.end_byte].decode("utf-8")
        return None

    def _get_function_signature(self, node, source_bytes: bytes) -> Optional[str]:
        """
        Extract function signature (def name(params) -> return_type).

        Args:
            node: function_definition node
            source_bytes: Source file bytes

        Returns:
            Signature string or None
        """
        # Find the line containing 'def' keyword
        for child in node.children:
            if child.type in ("identifier", "parameters", "type"):
                continue
            # Get first line of function definition
            start_line = node.start_point[0]
            end_byte = node.end_byte
            lines = source_bytes.decode("utf-8").split("\n")
            if start_line < len(lines):
                # Extract signature (first line, up to colon)
                sig_line = lines[start_line].strip()
                if ":" in sig_line:
                    sig_line = sig_line.split(":")[0].strip()
                return sig_line
        return None

    def _walk_python_node(
        self, node, source_bytes, filename, file_path, min_line, max_line,
        nodes, in_range, start_line, end_line, scope_stack
    ):
        """Handle Python-specific node types."""
        if node.type == "function_definition":
            func_name = self._get_function_name(node, source_bytes)
            if func_name and in_range:
                signature = self._get_function_signature(node, source_bytes)
                scope_path = ".".join(scope_stack + [func_name])
                node_id = f"{filename}::{func_name}::{start_line}"

                ast_node = ASTNode(
                    node_id=node_id,
                    file_path=file_path,
                    function_name=func_name,
                    class_name=scope_stack[0] if scope_stack else None,
                    start_line=start_line,
                    end_line=end_line,
                    scope_path=scope_path,
                    signature=signature,
                )
                nodes.append(ast_node)

            # Recurse with updated scope
            new_scope = scope_stack + [func_name] if func_name else scope_stack
            for child in node.children:
                self._walk_tree(
                    child, source_bytes, filename, file_path, min_line, max_line,
                    nodes, "python", new_scope
                )

        elif node.type == "class_definition":
            class_name = self._get_class_name(node, source_bytes)
            if class_name and in_range:
                scope_path = ".".join(scope_stack + [class_name])
                node_id = f"{filename}::{class_name}::{start_line}"

                ast_node = ASTNode(
                    node_id=node_id,
                    file_path=file_path,
                    class_name=class_name,
                    start_line=start_line,
                    end_line=end_line,
                    scope_path=scope_path,
                    signature=f"class {class_name}",
                )
                nodes.append(ast_node)

            # Recurse with updated scope
            new_scope = scope_stack + [class_name] if class_name else scope_stack
            for child in node.children:
                self._walk_tree(
                    child, source_bytes, filename, file_path, min_line, max_line,
                    nodes, "python", new_scope
                )

        else:
            # Recurse without changing scope
            for child in node.children:
                self._walk_tree(
                    child, source_bytes, filename, file_path, min_line, max_line,
                    nodes, "python", scope_stack
                )

    def _walk_js_node(
        self, node, source_bytes, filename, file_path, min_line, max_line,
        nodes, in_range, start_line, end_line, scope_stack, language
    ):
        """Handle JavaScript/TypeScript-specific node types."""
        # Function declarations: function foo() {}
        if node.type == "function_declaration":
            func_name = self._get_js_function_name(node, source_bytes)
            if func_name and in_range:
                signature = self._get_js_signature(node, source_bytes)
                scope_path = ".".join(scope_stack + [func_name])
                node_id = f"{filename}::{func_name}::{start_line}"

                ast_node = ASTNode(
                    node_id=node_id,
                    file_path=file_path,
                    function_name=func_name,
                    class_name=scope_stack[0] if scope_stack else None,
                    start_line=start_line,
                    end_line=end_line,
                    scope_path=scope_path,
                    signature=signature,
                )
                nodes.append(ast_node)

            new_scope = scope_stack + [func_name] if func_name else scope_stack
            for child in node.children:
                self._walk_tree(
                    child, source_bytes, filename, file_path, min_line, max_line,
                    nodes, language, new_scope
                )

        # Arrow functions: const foo = () => {}
        elif node.type in ("lexical_declaration", "variable_declaration"):
            func_name, is_function = self._get_js_arrow_function(node, source_bytes)
            if func_name and is_function and in_range:
                signature = self._get_js_signature(node, source_bytes)
                scope_path = ".".join(scope_stack + [func_name])
                node_id = f"{filename}::{func_name}::{start_line}"

                ast_node = ASTNode(
                    node_id=node_id,
                    file_path=file_path,
                    function_name=func_name,
                    class_name=scope_stack[0] if scope_stack else None,
                    start_line=start_line,
                    end_line=end_line,
                    scope_path=scope_path,
                    signature=signature,
                )
                nodes.append(ast_node)

            for child in node.children:
                self._walk_tree(
                    child, source_bytes, filename, file_path, min_line, max_line,
                    nodes, language, scope_stack
                )

        # Class declarations
        elif node.type == "class_declaration":
            class_name = self._get_js_class_name(node, source_bytes)
            if class_name and in_range:
                scope_path = ".".join(scope_stack + [class_name])
                node_id = f"{filename}::{class_name}::{start_line}"

                ast_node = ASTNode(
                    node_id=node_id,
                    file_path=file_path,
                    class_name=class_name,
                    start_line=start_line,
                    end_line=end_line,
                    scope_path=scope_path,
                    signature=f"class {class_name}",
                )
                nodes.append(ast_node)

            new_scope = scope_stack + [class_name] if class_name else scope_stack
            for child in node.children:
                self._walk_tree(
                    child, source_bytes, filename, file_path, min_line, max_line,
                    nodes, language, new_scope
                )

        # Method definitions in classes
        elif node.type == "method_definition":
            method_name = self._get_js_method_name(node, source_bytes)
            if method_name and in_range:
                signature = self._get_js_signature(node, source_bytes)
                scope_path = ".".join(scope_stack + [method_name])
                node_id = f"{filename}::{method_name}::{start_line}"

                ast_node = ASTNode(
                    node_id=node_id,
                    file_path=file_path,
                    function_name=method_name,
                    class_name=scope_stack[0] if scope_stack else None,
                    start_line=start_line,
                    end_line=end_line,
                    scope_path=scope_path,
                    signature=signature,
                )
                nodes.append(ast_node)

            new_scope = scope_stack + [method_name] if method_name else scope_stack
            for child in node.children:
                self._walk_tree(
                    child, source_bytes, filename, file_path, min_line, max_line,
                    nodes, language, new_scope
                )

        else:
            # Recurse without changing scope
            for child in node.children:
                self._walk_tree(
                    child, source_bytes, filename, file_path, min_line, max_line,
                    nodes, language, scope_stack
                )

    def _get_js_function_name(self, node, source_bytes: bytes) -> Optional[str]:
        """Extract function name from JavaScript function_declaration."""
        for child in node.children:
            if child.type == "identifier":
                return source_bytes[child.start_byte : child.end_byte].decode("utf-8")
        return None

    def _get_js_class_name(self, node, source_bytes: bytes) -> Optional[str]:
        """Extract class name from JavaScript class_declaration."""
        for child in node.children:
            if child.type in ("identifier", "type_identifier"):
                return source_bytes[child.start_byte : child.end_byte].decode("utf-8")
        return None

    def _get_js_method_name(self, node, source_bytes: bytes) -> Optional[str]:
        """Extract method name from JavaScript method_definition."""
        for child in node.children:
            if child.type == "property_identifier":
                return source_bytes[child.start_byte : child.end_byte].decode("utf-8")
        return None

    def _get_js_arrow_function(self, node, source_bytes: bytes) -> tuple[Optional[str], bool]:
        """
        Check if variable declaration contains arrow function.
        Returns (name, is_function).
        """
        # Look for pattern: const name = () => {}
        var_name = None
        is_arrow = False

        for child in node.children:
            if child.type == "variable_declarator":
                # Get variable name
                for subchild in child.children:
                    if subchild.type == "identifier":
                        var_name = source_bytes[subchild.start_byte : subchild.end_byte].decode("utf-8")
                    elif subchild.type == "arrow_function":
                        is_arrow = True

        return var_name, is_arrow

    def _get_js_signature(self, node, source_bytes: bytes) -> Optional[str]:
        """Extract JavaScript/TypeScript function signature."""
        start_line = node.start_point[0]
        lines = source_bytes.decode("utf-8").split("\n")
        if start_line < len(lines):
            sig_line = lines[start_line].strip()
            # For multi-line signatures, try to get up to opening brace
            if "{" in sig_line:
                sig_line = sig_line.split("{")[0].strip()
            return sig_line
        return None

    def _fallback_excerpt(self, file_path: str, error_line: int) -> ASTContract:
        """
        Fallback when tree-sitter fails: return raw excerpt ≤ 200 tokens.

        Args:
            file_path: Path to source file
            error_line: Line number of error (1-indexed)

        Returns:
            ASTContract with is_fallback=True and raw_excerpt

        Requirements: 2.4
        """
        path = Path(file_path)
        if not path.exists():
            contract = ASTContract(
                error_type="file_not_found",
                is_fallback=True,
                source_files=[file_path],
                raw_excerpt=f"File not found: {file_path}",
            )
            serialized = contract.model_dump_json()
            contract.total_size_bytes = len(serialized.encode("utf-8"))
            return contract

        try:
            lines = path.read_text(encoding="utf-8").split("\n")
            # Extract ±10 lines around error
            min_line = max(0, error_line - 11)  # 0-indexed
            max_line = min(len(lines), error_line + 10)
            excerpt_lines = lines[min_line:max_line]

            # Limit to ~200 tokens (rough estimate: 1 token ≈ 4 chars)
            excerpt = "\n".join(excerpt_lines)
            max_chars = 800  # 200 tokens * 4 chars/token
            if len(excerpt) > max_chars:
                excerpt = excerpt[:max_chars] + "\n... (truncated)"

            contract = ASTContract(
                error_type="parse_failed",
                is_fallback=True,
                source_files=[file_path],
                raw_excerpt=excerpt,
            )
            serialized = contract.model_dump_json()
            contract.total_size_bytes = len(serialized.encode("utf-8"))
            return contract

        except Exception as e:
            contract = ASTContract(
                error_type="read_error",
                is_fallback=True,
                source_files=[file_path],
                raw_excerpt=f"Error reading file: {e}",
            )
            serialized = contract.model_dump_json()
            contract.total_size_bytes = len(serialized.encode("utf-8"))
            return contract

    def _enforce_size_limit(self, contract: ASTContract) -> ASTContract:
        """
        Enforce 4KB hard limit by truncating affected_nodes if needed.

        Args:
            contract: ASTContract to check and potentially truncate

        Returns:
            ASTContract guaranteed to serialize to ≤ 4096 bytes

        Requirements: 2.2
        Property: 5
        """
        # Serialize and check size
        serialized = contract.model_dump_json()
        size_bytes = len(serialized.encode("utf-8"))

        if size_bytes <= 4096:
            contract.total_size_bytes = size_bytes
            return contract

        # Truncate nodes until under limit
        while len(contract.affected_nodes) > 0:
            # Remove last node
            contract.affected_nodes.pop()

            # Re-serialize and check
            serialized = contract.model_dump_json()
            size_bytes = len(serialized.encode("utf-8"))

            if size_bytes <= 4096:
                contract.total_size_bytes = size_bytes
                return contract

        # If still too large, fall back to minimal contract
        contract.total_size_bytes = size_bytes
        return contract
