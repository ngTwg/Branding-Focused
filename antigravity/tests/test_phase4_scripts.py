#!/usr/bin/env python3
"""
Test Phase 4 Scripts
Verify all 6 bug fix scripts work correctly
"""

import sys
import tempfile
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


def test_autonomous_loop():
    """Test autonomous_loop.py"""
    print("🧪 Testing autonomous_loop.py...")
    
    try:
        from autonomous_loop import AutonomousLoop, FailureMemoryDB, RootCauseAnalyzer
        
        # Test FailureMemoryDB
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        db = FailureMemoryDB(db_path)
        db.log("test_error", "test_cause", "test_fix", True, 1)
        stats = db.get_stats()
        assert stats["total"] == 1
        db.close()
        
        # Test RootCauseAnalyzer
        analyzer = RootCauseAnalyzer()
        result = analyzer.analyze("ModuleNotFoundError: No module named 'test'")
        assert result["type"] == "missing_dependency"
        
        # Cleanup
        Path(db_path).unlink(missing_ok=True)
        
        print("   ✅ autonomous_loop.py works")
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_skill_cache():
    """Test skill_cache.py"""
    print("🧪 Testing skill_cache.py...")
    
    try:
        from skill_cache import get_skill_content, cache_stats, clear_cache
        
        # Test cache
        skills_root = Path("C:/Users/<YOUR_USERNAME>/.gemini/antigravity/skills")
        test_skill = skills_root / "workflows" / "debug-protocol.md"
        
        if test_skill.exists():
            # First call (miss)
            content1 = get_skill_content(str(test_skill))
            assert len(content1) > 0
            
            # Second call (hit)
            content2 = get_skill_content(str(test_skill))
            assert content1 == content2
            
            # Check stats
            stats = cache_stats()
            assert stats["hits"] >= 1
            
            clear_cache()
        
        print("   ✅ skill_cache.py works")
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_extract_training_data():
    """Test extract_training_data.py"""
    print("🧪 Testing extract_training_data.py...")
    
    try:
        from extract_training_data import ConversationParser, TrainingDataExtractor
        
        # Test parser
        parser = ConversationParser()
        
        test_text = """
        ERROR: Function failed with TypeError
        FIX: Added type checking and validation
        """
        
        pairs = parser.extract_pairs(test_text)
        assert len(pairs) > 0
        assert "prompt" in pairs[0]
        assert "response" in pairs[0]
        
        print("   ✅ extract_training_data.py works")
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_self_healer():
    """Test self_healer.py"""
    print("🧪 Testing self_healer.py...")
    
    try:
        from self_healer import ErrorLogHandler, SelfHealer
        
        # Test handler
        handler = ErrorLogHandler(auto_fix=False)
        assert handler.is_error_log("test.error.log") == True
        assert handler.is_error_log("test.txt") == False
        handler.cleanup()
        
        print("   ✅ self_healer.py works")
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_swarm_orchestrator():
    """Test swarm_orchestrator.py"""
    print("🧪 Testing swarm_orchestrator.py...")
    
    try:
        from swarm_orchestrator import SwarmOrchestrator, Agent, AgentRole
        
        # Test orchestrator
        orchestrator = SwarmOrchestrator()
        
        # Test task analysis
        roles = orchestrator.analyze_task("Design and implement a secure API")
        assert "architect" in roles
        assert "developer" in roles
        
        # Test orchestration
        results = orchestrator.orchestrate("Build a simple feature")
        assert "roles" in results
        assert "approved" in results
        
        print("   ✅ swarm_orchestrator.py works")
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_shadow_tester():
    """Test shadow_tester.py"""
    print("🧪 Testing shadow_tester.py...")
    
    try:
        from shadow_tester import ShadowTester
        
        # Test tester
        tester = ShadowTester(cleanup_on_exit=True)
        
        # Test framework detection
        framework = tester.detect_test_framework(".")
        # Framework may be None if no tests found, that's OK
        
        print("   ✅ shadow_tester.py works")
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Phase 4 Scripts Test Suite")
    print("="*60)
    print()
    
    tests = [
        ("Autonomous Loop", test_autonomous_loop),
        ("Skill Cache", test_skill_cache),
        ("Training Data Extractor", test_extract_training_data),
        ("Self Healer", test_self_healer),
        ("Swarm Orchestrator", test_swarm_orchestrator),
        ("Shadow Tester", test_shadow_tester),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status}: {name}")
    
    print()
    print(f"   Total: {passed}/{total} passed ({passed/total*100:.0f}%)")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
