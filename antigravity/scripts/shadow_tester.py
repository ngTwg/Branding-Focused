#!/usr/bin/env python3
"""
Shadow Testing Environment
Create isolated shadow copies of projects for safe testing

Features:
- Create temporary shadow copies
- Run tests in isolation
- Automatic cleanup
- Support for multiple test frameworks (pytest, jest, vitest)
"""

import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, Optional, List
import time


class ShadowTester:
    """Shadow testing environment manager"""
    
    def __init__(self, cleanup_on_exit: bool = True):
        self.cleanup_on_exit = cleanup_on_exit
        self.shadow_paths = []
    
    def create_shadow(self, project_path: str, exclude: List[str] = None) -> str:
        """
        Create shadow copy of project
        
        Args:
            project_path: Path to original project
            exclude: List of patterns to exclude (e.g., node_modules, .git)
        
        Returns:
            Path to shadow directory
        """
        project_path = Path(project_path).resolve()
        
        if not project_path.exists():
            raise FileNotFoundError(f"Project not found: {project_path}")
        
        print(f"🌑 Creating shadow copy of: {project_path.name}")
        
        # Create temp directory
        shadow = tempfile.mkdtemp(prefix="antigravity_shadow_")
        shadow_path = Path(shadow)
        
        print(f"   Shadow location: {shadow_path}")
        
        # Default exclusions
        if exclude is None:
            exclude = [
                "node_modules",
                ".git",
                ".venv",
                "venv",
                "__pycache__",
                ".pytest_cache",
                "dist",
                "build",
                ".next",
                ".nuxt",
                "coverage"
            ]
        
        # Copy project with exclusions
        def ignore_patterns(directory, files):
            """Ignore function for shutil.copytree"""
            ignored = []
            for pattern in exclude:
                if pattern in files:
                    ignored.append(pattern)
            return ignored
        
        try:
            shutil.copytree(
                project_path,
                shadow_path / project_path.name,
                ignore=ignore_patterns,
                dirs_exist_ok=True
            )
            
            actual_shadow = shadow_path / project_path.name
            self.shadow_paths.append(actual_shadow)
            
            print(f"   ✅ Shadow created: {actual_shadow}")
            return str(actual_shadow)
        
        except Exception as e:
            print(f"   ❌ Error creating shadow: {e}")
            shutil.rmtree(shadow_path, ignore_errors=True)
            raise
    
    def detect_test_framework(self, shadow_path: str) -> Optional[str]:
        """
        Detect test framework used in project
        
        Args:
            shadow_path: Path to shadow directory
        
        Returns:
            Test framework name or None
        """
        shadow = Path(shadow_path)
        
        # Check for Python pytest
        if (shadow / "pytest.ini").exists() or \
           (shadow / "setup.py").exists() or \
           list(shadow.rglob("test_*.py")):
            return "pytest"
        
        # Check for JavaScript/TypeScript
        package_json = shadow / "package.json"
        if package_json.exists():
            try:
                import json
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                    
                    if "vitest" in deps:
                        return "vitest"
                    elif "jest" in deps:
                        return "jest"
                    elif "@playwright/test" in deps:
                        return "playwright"
            except Exception:
                pass
        
        return None
    
    def run_tests(self, shadow_path: str, framework: str = None, 
                  timeout: int = 120) -> Dict:
        """
        Run tests in shadow environment
        
        Args:
            shadow_path: Path to shadow directory
            framework: Test framework (auto-detect if None)
            timeout: Timeout in seconds
        
        Returns:
            Dict with test results
        """
        shadow = Path(shadow_path)
        
        if not shadow.exists():
            raise FileNotFoundError(f"Shadow not found: {shadow_path}")
        
        # Auto-detect framework
        if framework is None:
            framework = self.detect_test_framework(shadow_path)
            if framework is None:
                print("⚠️ Could not detect test framework")
                return {
                    "success": False,
                    "framework": "unknown",
                    "output": "No test framework detected"
                }
        
        print(f"🧪 Running tests with {framework}...")
        
        # Build command based on framework
        commands = {
            "pytest": ["python", "-m", "pytest", "--tb=short", "-q"],
            "jest": ["npm", "test", "--", "--ci", "--silent"],
            "vitest": ["npm", "test", "--", "--run", "--silent"],
            "playwright": ["npx", "playwright", "test"]
        }
        
        cmd = commands.get(framework)
        if not cmd:
            return {
                "success": False,
                "framework": framework,
                "output": f"Unknown framework: {framework}"
            }
        
        # Run tests
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                cwd=shadow_path,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            elapsed = time.time() - start_time
            
            # Truncate output
            output = result.stdout + result.stderr
            if len(output) > 1500:
                output = output[-1500:] + "\n... (truncated)"
            
            success = result.returncode == 0
            
            print(f"   {'✅' if success else '❌'} Tests {'passed' if success else 'failed'} ({elapsed:.1f}s)")
            
            return {
                "success": success,
                "framework": framework,
                "returncode": result.returncode,
                "output": output,
                "elapsed": elapsed
            }
        
        except subprocess.TimeoutExpired:
            print(f"   ⏱️ Tests timed out after {timeout}s")
            return {
                "success": False,
                "framework": framework,
                "returncode": -1,
                "output": f"Timeout after {timeout}s",
                "elapsed": timeout
            }
        
        except Exception as e:
            print(f"   ❌ Error running tests: {e}")
            return {
                "success": False,
                "framework": framework,
                "output": str(e),
                "elapsed": time.time() - start_time
            }
    
    def cleanup(self, shadow_path: str = None):
        """
        Clean up shadow directory
        
        Args:
            shadow_path: Specific shadow to clean (None = all)
        """
        if shadow_path:
            path = Path(shadow_path)
            if path.exists():
                shutil.rmtree(path, ignore_errors=True)
                print(f"🧹 Cleaned: {path}")
                if path in self.shadow_paths:
                    self.shadow_paths.remove(path)
        else:
            # Clean all shadows
            for path in self.shadow_paths:
                if path.exists():
                    shutil.rmtree(path, ignore_errors=True)
                    print(f"🧹 Cleaned: {path}")
            self.shadow_paths.clear()
    
    def __del__(self):
        """Cleanup on deletion"""
        if self.cleanup_on_exit:
            self.cleanup()


def main():
    """CLI entry point"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Shadow Testing Environment - Safe isolated testing"
    )
    parser.add_argument(
        "project_path",
        help="Path to project to test"
    )
    parser.add_argument(
        "--framework",
        choices=["pytest", "jest", "vitest", "playwright"],
        help="Test framework (auto-detect if not specified)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Test timeout in seconds (default: 120)"
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Don't cleanup shadow after tests"
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        help="Additional patterns to exclude from shadow"
    )
    
    args = parser.parse_args()
    
    # Create tester
    tester = ShadowTester(cleanup_on_exit=not args.no_cleanup)
    
    try:
        # Create shadow
        shadow = tester.create_shadow(args.project_path, exclude=args.exclude)
        
        print()
        
        # Run tests
        results = tester.run_tests(
            shadow,
            framework=args.framework,
            timeout=args.timeout
        )
        
        print()
        print("📊 Results:")
        print(f"   Framework: {results['framework']}")
        print(f"   Success: {results['success']}")
        print(f"   Time: {results.get('elapsed', 0):.1f}s")
        
        if results.get('output'):
            print()
            print("📝 Output:")
            print(results['output'])
        
        # Cleanup
        if not args.no_cleanup:
            print()
            tester.cleanup(shadow)
        else:
            print()
            print(f"ℹ️ Shadow preserved at: {shadow}")
        
        # Exit code
        sys.exit(0 if results['success'] else 1)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Demo mode if no arguments
    import sys
    if len(sys.argv) == 1:
        print("🚀 Shadow Testing Environment Demo")
        print()
        print("Usage: python shadow_tester.py <project_path>")
        print()
        print("Example:")
        print("  python shadow_tester.py C:/Users/<YOUR_USERNAME>/.gemini/antigravity")
        print("  python shadow_tester.py . --framework pytest --timeout 60")
        sys.exit(0)
    
    main()
