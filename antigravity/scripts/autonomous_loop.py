#!/usr/bin/env python3
"""
E2E Autonomous Loop Closure (Consolidated v6.5.0)
DETECT Error → ANALYZE Root Cause → PLAN Fix → APPLY → VERIFY → LOG

Memory: Unified core.failure_memory (JSONL)
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# Add antigravity root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from antigravity.core.failure_memory import FailureMemory
from antigravity.core.pattern_extractor import PatternExtractorV2
from antigravity.core.schemas import FailureSurface
from antigravity.scripts.orchestrator import AntigravityOrchestrator

class AutonomousLoop:
    """Main autonomous loop controller - Using Unified Core Memory"""
    
    MAX_RETRIES = 3
    TIMEOUT = 300  # 5 minutes stagnation guard
    
    def __init__(self, storage_path: str = None):
        if storage_path is None:
            storage_path = PROJECT_ROOT / "brain" / "failure_memory.jsonl"
            
        self.memory = FailureMemory(storage_path=storage_path)
        self.extractor = PatternExtractorV2()
        self.orchestrator = AntigravityOrchestrator()
    
    def detect_error(self, log_path: str) -> Optional[str]:
        """Read and return log content"""
        path = Path(log_path)
        if not path.exists():
            return None
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return None
    
    def run(self, log_path: str, auto_fix: bool = False) -> Dict:
        """Main autonomous loop using unified memory"""
        print(f"🚀 [Unified] Autonomous Loop: {log_path}")
        
        start_time = time.time()
        retries = 0
        results = {"success": False, "retries": 0, "error_type": "unknown"}
        
        while retries < self.MAX_RETRIES:
            # Stagnation guard
            if (time.time() - start_time) > self.TIMEOUT:
                print("⚠️ STAGNATION GUARD: Timeout triggered")
                break
            
            print(f"🔄 Attempt {retries + 1}/{self.MAX_RETRIES}")
            
            # STEP 1: Detect error
            log_content = self.detect_error(log_path)
            if not log_content: break
            
            # STEP 2: Analyze & Retrieve Patterns
            # Create a mock surface for retrieval purposes
            surface = FailureSurface(
                failure_id=f"auto_{int(time.time())}",
                patch_diff="",
                error_text=log_content[:500],
                files_touched=[],
                timestamp=datetime.now().isoformat(),
                session_id="autonomous_loop"
            )
            
            # Search relevant patterns from unified core memory
            relevant = self.memory.retrieve_lessons("Reparing detected log error", log_content[:500])
            
            if relevant:
                print(f"   📚 Found {len(relevant)} relevant patterns in Core Memory")
                for i, (p, l, s) in enumerate(relevant, 1):
                    print(f"      [{s:.0%}] {p.cause}: {l.prefer}")
            
            # STEP 3: Planning & Execution (Consolidated v6.5)
            # Call AntigravityOrchestrator to execute the fix
            repair_task = {
                "description": f"Fix error log: {log_path}\nError Content: {log_content[:1000]}",
                "intent": "debug",
                "domain": "debug"
            }
            
            if auto_fix:
                print("   🛠️  Executing Autonomous Repair...")
                try:
                    result = self.orchestrator.execute(repair_task)
                    if result.get("status") == "success":
                        print("   ✅ Repair execution successful!")
                        results["success"] = True
                        break
                    else:
                        print(f"   ❌ Repair failed: {result.get('reason', 'Unknown error')}")
                except Exception as e:
                    print(f"   ❌ Orchestrator Error: {e}")
            else:
                print("   ⏸️ Manual fix required")
                break
            
            time.sleep(1)
            
        results["retries"] = retries
        results["time_elapsed"] = time.time() - start_time
        return results
    
    def close(self):
        """Cleanup"""
        pass

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file")
    parser.add_argument("--auto-fix", action="store_true")
    args = parser.parse_args()
    
    loop = AutonomousLoop()
    loop.run(args.log_file, auto_fix=args.auto_fix)

if __name__ == "__main__":
    main()
