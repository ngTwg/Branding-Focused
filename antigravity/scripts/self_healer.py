#!/usr/bin/env python3
"""
Self-Healing Code Watcher
Automatically detect error logs and trigger autonomous loop

Features:
- Watch multiple directories for error logs
- Auto-trigger autonomous_loop.py on error detection
- Graceful shutdown (Ctrl+C)
- Configurable error patterns
"""

import sys
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

# Import autonomous loop
try:
    from autonomous_loop import AutonomousLoop
except ImportError:
    print("⚠️ autonomous_loop.py not found in same directory")
    print("   Make sure autonomous_loop.py is in the same folder")
    sys.exit(1)


# Configuration
ERROR_PATTERNS = [
    ".error.log",
    ".stderr",
    "npm-debug.log",
    "error.txt",
    "crash.log",
    "exception.log",
]

WATCH_PATHS = [
    "C:/Users/<YOUR_USERNAME>/.gemini/antigravity",
]


class ErrorLogHandler(FileSystemEventHandler):
    """Handle file system events for error logs"""
    
    def __init__(self, auto_fix: bool = False):
        super().__init__()
        self.auto_fix = auto_fix
        self.loop = AutonomousLoop()
        self.processed = set()  # Avoid duplicate processing
    
    def is_error_log(self, path: str) -> bool:
        """Check if file is an error log"""
        path_lower = path.lower()
        return any(pattern in path_lower for pattern in ERROR_PATTERNS)
    
    def on_modified(self, event: FileModifiedEvent):
        """Handle file modification events"""
        if event.is_directory:
            return
        
        path = str(event.src_path)
        
        # Check if it's an error log
        if not self.is_error_log(path):
            return
        
        # Avoid duplicate processing
        if path in self.processed:
            return
        
        print()
        print("🚨 " + "="*60)
        print(f"   Error log detected: {Path(path).name}")
        print("   " + "="*60)
        print()
        
        # Mark as processed
        self.processed.add(path)
        
        # Trigger autonomous loop
        try:
            results = self.loop.run(path, auto_fix=self.auto_fix)
            
            if results["success"]:
                print()
                print("✅ Self-healing successful!")
            else:
                print()
                print("⚠️ Self-healing incomplete - manual intervention may be needed")
        
        except Exception as e:
            print(f"❌ Error during self-healing: {e}")
        
        # Remove from processed after some time to allow re-processing
        # if the file is modified again
        time.sleep(5)
        if path in self.processed:
            self.processed.remove(path)
    
    def cleanup(self):
        """Cleanup resources"""
        self.loop.close()


class SelfHealer:
    """Main self-healer class"""
    
    def __init__(self, watch_paths: list, auto_fix: bool = False):
        self.watch_paths = [Path(p) for p in watch_paths]
        self.auto_fix = auto_fix
        self.observer = Observer()
        self.handler = ErrorLogHandler(auto_fix=auto_fix)
    
    def start(self):
        """Start watching for error logs"""
        print("👁️ Self-Healing Code Watcher")
        print(f"   Auto-fix: {'Enabled' if self.auto_fix else 'Disabled'}")
        print(f"   Watching {len(self.watch_paths)} paths:")
        
        for path in self.watch_paths:
            if not path.exists():
                print(f"   ⚠️ Path not found: {path}")
                continue
            
            print(f"   📁 {path}")
            self.observer.schedule(self.handler, str(path), recursive=True)
        
        print()
        print("   Error patterns:")
        for pattern in ERROR_PATTERNS:
            print(f"   - {pattern}")
        
        print()
        print("✅ Watcher started. Press Ctrl+C to stop.")
        print()
        
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print()
            print("🛑 Stopping watcher...")
            self.stop()
    
    def stop(self):
        """Stop watching"""
        self.observer.stop()
        self.observer.join()
        self.handler.cleanup()
        print("✅ Watcher stopped")


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Self-Healing Code Watcher - Auto-detect and fix errors"
    )
    parser.add_argument(
        "--auto-fix",
        action="store_true",
        help="Enable automatic fixing (experimental)"
    )
    parser.add_argument(
        "--watch",
        nargs="+",
        default=WATCH_PATHS,
        help="Paths to watch (default: antigravity root)"
    )
    parser.add_argument(
        "--patterns",
        nargs="+",
        help="Custom error log patterns (default: .error.log, .stderr, etc.)"
    )
    
    args = parser.parse_args()
    
    # Override patterns if provided
    if args.patterns:
        global ERROR_PATTERNS
        ERROR_PATTERNS = args.patterns
    
    # Create and start healer
    healer = SelfHealer(
        watch_paths=args.watch,
        auto_fix=args.auto_fix
    )
    
    healer.start()


if __name__ == "__main__":
    main()
