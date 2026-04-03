#!/usr/bin/env python3
"""
Multi-Agent Swarm Orchestrator
Spawn specialized agents for different roles and coordinate their work

Features:
- 5 agent roles: architect, developer, reviewer, tester, security
- Keyword-based task analysis
- Peer review mechanism
- Conflict resolution
- Approval tracking
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class AgentRole(Enum):
    """Agent role types"""
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    TESTER = "tester"
    SECURITY = "security"


# Agent role configurations
AGENT_ROLES = {
    "architect": {
        "keywords": ["design", "architecture", "schema", "structure", "plan", "blueprint"],
        "skills": [
            "api-design-standards",
            "database-standards",
            "state-classification",
            "documentation-standards"
        ],
        "priority": 1  # Execute first
    },
    "developer": {
        "keywords": ["implement", "build", "code", "write", "create", "develop"],
        "skills": [
            "react-best-practices",
            "error-handling-patterns",
            "naming-conventions",
            "anti-hallucination-v2"
        ],
        "priority": 2  # Execute after architect
    },
    "reviewer": {
        "keywords": ["review", "audit", "check", "verify", "inspect", "validate"],
        "skills": [
            "security-middleware-stack",
            "refactoring-triggers",
            "edge-case-catalog"
        ],
        "priority": 3  # Execute after developer
    },
    "tester": {
        "keywords": ["test", "qa", "coverage", "unit", "integration", "e2e"],
        "skills": [
            "edge-case-catalog",
            "debug-protocol",
            "error-handling-patterns"
        ],
        "priority": 3  # Parallel with reviewer
    },
    "security": {
        "keywords": ["security", "pentest", "vulnerability", "exploit", "attack", "defense"],
        "skills": [
            "security-master-inventory",
            "security-middleware-stack",
            "vulnerability-scanner"
        ],
        "priority": 4  # Execute last (final check)
    }
}


@dataclass
class AgentResult:
    """Result from an agent execution"""
    role: str
    output: str = ""
    approved: bool = False
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    execution_time: float = 0.0


@dataclass
class SwarmTask:
    """Task to be executed by swarm"""
    description: str
    required_roles: List[str] = field(default_factory=list)
    context: Dict = field(default_factory=dict)


class Agent:
    """Individual agent"""
    
    def __init__(self, role: str, config: Dict):
        self.role = role
        self.config = config
        self.skills = config.get("skills", [])
    
    def execute(self, task: SwarmTask) -> AgentResult:
        """
        Execute task based on role
        
        Args:
            task: Task to execute
        
        Returns:
            AgentResult with output and approval status
        """
        result = AgentResult(role=self.role)
        
        # Simulate agent work (in real implementation, this would call actual tools)
        if self.role == "architect":
            result.output = f"[{self.role}] Designed architecture for: {task.description[:50]}"
            result.approved = True
        
        elif self.role == "developer":
            result.output = f"[{self.role}] Implemented: {task.description[:50]}"
            result.approved = True
        
        elif self.role == "reviewer":
            result.output = f"[{self.role}] Reviewed code"
            # Simulate finding issues
            result.issues = ["Missing error handling in function X"]
            result.approved = len(result.issues) == 0
        
        elif self.role == "tester":
            result.output = f"[{self.role}] Ran tests"
            result.approved = True
        
        elif self.role == "security":
            result.output = f"[{self.role}] Security audit complete"
            result.approved = True
        
        return result
    
    def peer_review(self, other_result: AgentResult) -> bool:
        """
        Review another agent's result
        
        Args:
            other_result: Result from another agent
        
        Returns:
            True if approved, False otherwise
        """
        # Simple validation: check if output is not empty
        if not other_result.output:
            return False
        
        # Role-specific review logic
        if self.role == "reviewer":
            # Reviewer is strict
            return len(other_result.output) > 50 and other_result.approved
        
        elif self.role == "security":
            # Security checks for security keywords
            security_keywords = ["secure", "validate", "sanitize", "encrypt"]
            return any(kw in other_result.output.lower() for kw in security_keywords)
        
        # Default: approve if output exists
        return len(other_result.output) > 0


class SwarmOrchestrator:
    """Main orchestrator for multi-agent swarm"""
    
    def __init__(self):
        self.agents = {
            role: Agent(role, config)
            for role, config in AGENT_ROLES.items()
        }
    
    def analyze_task(self, task_description: str) -> List[str]:
        """
        Analyze task and determine required agent roles
        
        Args:
            task_description: Task description text
        
        Returns:
            List of required agent roles
        """
        task_lower = task_description.lower()
        roles = []
        
        for role, config in AGENT_ROLES.items():
            keywords = config.get("keywords", [])
            if any(keyword in task_lower for keyword in keywords):
                roles.append(role)
        
        # If no roles matched, default to developer
        if not roles:
            roles = ["developer"]
        
        # Always add reviewer if not present
        if "reviewer" not in roles and len(roles) > 0:
            roles.append("reviewer")
        
        # Sort by priority
        roles.sort(key=lambda r: AGENT_ROLES[r].get("priority", 99))
        
        return roles
    
    def execute_swarm(self, task: SwarmTask) -> Dict:
        """
        Execute task with swarm of agents
        
        Args:
            task: Task to execute
        
        Returns:
            Dict with execution results
        """
        print(f"🤖 Spawning swarm for: {task.description[:60]}...")
        
        # Determine required roles
        if not task.required_roles:
            task.required_roles = self.analyze_task(task.description)
        
        print(f"   Roles: {', '.join(task.required_roles)}")
        print()
        
        results = []
        
        # Execute agents in priority order
        for role in task.required_roles:
            agent = self.agents.get(role)
            if not agent:
                print(f"   ⚠️ Unknown role: {role}")
                continue
            
            print(f"   🔄 {role.upper()} executing...")
            result = agent.execute(task)
            
            # Peer review by other agents
            approvals = 0
            for other_role, other_agent in self.agents.items():
                if other_role != role:
                    if other_agent.peer_review(result):
                        approvals += 1
            
            result.approved = result.approved and (approvals >= 2)
            
            status = "✅" if result.approved else "⚠️"
            print(f"   {status} {role.upper()}: {result.output[:60]}")
            
            if result.issues:
                print(f"      Issues: {', '.join(result.issues)}")
            
            results.append(result)
        
        # Calculate overall approval
        approved_count = sum(1 for r in results if r.approved)
        total_count = len(results)
        approval_rate = (approved_count / total_count * 100) if total_count > 0 else 0
        
        print()
        print(f"📊 Swarm Results:")
        print(f"   Approved: {approved_count}/{total_count} ({approval_rate:.0f}%)")
        
        return {
            "task": task.description,
            "roles": task.required_roles,
            "results": results,
            "approved": approved_count,
            "total": total_count,
            "approval_rate": approval_rate,
            "success": approval_rate >= 80  # 80% approval threshold
        }
    
    def orchestrate(self, task_description: str, context: Dict = None) -> Dict:
        """
        Orchestrate swarm for a task description
        
        Args:
            task_description: Task description
            context: Optional context dict
        
        Returns:
            Dict with results
        """
        task = SwarmTask(
            description=task_description,
            context=context or {}
        )
        
        return self.execute_swarm(task)
    
    def resolve_conflict(self, results: List[AgentResult]) -> AgentResult:
        """
        Resolve conflicts between agent results
        
        Args:
            results: List of conflicting results
        
        Returns:
            Resolved result (lead agent decision)
        """
        # Priority-based resolution: architect > security > reviewer > developer > tester
        priority_order = ["architect", "security", "reviewer", "developer", "tester"]
        
        for role in priority_order:
            for result in results:
                if result.role == role:
                    print(f"🎯 Conflict resolved by: {role.upper()}")
                    return result
        
        # Fallback: return first result
        return results[0] if results else AgentResult(role="unknown")


def main():
    """CLI entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python swarm_orchestrator.py <task_description>")
        print()
        print("Examples:")
        print('  python swarm_orchestrator.py "Design and implement a secure REST API"')
        print('  python swarm_orchestrator.py "Review code for security vulnerabilities"')
        print('  python swarm_orchestrator.py "Build React component with tests"')
        sys.exit(1)
    
    task_description = " ".join(sys.argv[1:])
    
    orchestrator = SwarmOrchestrator()
    results = orchestrator.orchestrate(task_description)
    
    # Exit code based on success
    sys.exit(0 if results["success"] else 1)


if __name__ == "__main__":
    # Demo mode if no arguments
    import sys
    if len(sys.argv) == 1:
        print("🚀 Multi-Agent Swarm Orchestrator Demo")
        print()
        
        orchestrator = SwarmOrchestrator()
        
        # Test case 1
        print("=" * 70)
        print("Test 1: Full-stack development")
        print("=" * 70)
        orchestrator.orchestrate(
            "Implement and review a secure REST API with authentication tests"
        )
        
        print()
        print("=" * 70)
        print("Test 2: Security audit")
        print("=" * 70)
        orchestrator.orchestrate(
            "Security audit and penetration testing of payment system"
        )
        
        print()
        print("=" * 70)
        print("Test 3: Code review")
        print("=" * 70)
        orchestrator.orchestrate(
            "Review React component code for best practices and test coverage"
        )
    else:
        main()
