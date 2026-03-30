#!/usr/bin/env python3
"""
AUTOMATION TESTING FOR SKILLS SYSTEM
Validates 544+ skills for consistency, correctness, and maintainability
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple
import yaml

# Base paths
SKILLS_ROOT = Path("antigravity/skills")
KIRO_RULES = Path(".kiro/steering/KIRO.md")

class SkillValidator:
    """Validates individual skill files"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_skill_file(self, skill_path: Path) -> Tuple[bool, List[str], List[str]]:
        """Validate a single skill file"""
        self.errors = []
        self.warnings = []
        
        if not skill_path.exists():
            self.errors.append(f"File not found: {skill_path}")
            return False, self.errors, self.warnings
            
        content = skill_path.read_text(encoding='utf-8')
        
        # Run all validation checks
        self._check_frontmatter(content, skill_path)
        self._check_structure(content, skill_path)
        self._check_code_examples(content, skill_path)
        self._check_links(content, skill_path)
        self._check_rules_format(content, skill_path)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _check_frontmatter(self, content: str, path: Path):
        """Check YAML frontmatter if present"""
        if content.startswith('---'):
            try:
                # Extract frontmatter
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    
                    # Check required fields
                    if 'name' not in frontmatter:
                        self.warnings.append(f"{path.name}: Missing 'name' in frontmatter")
                    if 'description' not in frontmatter:
                        self.warnings.append(f"{path.name}: Missing 'description' in frontmatter")
                        
            except yaml.YAMLError as e:
                self.errors.append(f"{path.name}: Invalid YAML frontmatter: {e}")
    
    def _check_structure(self, content: str, path: Path):
        """Check document structure"""
        # Check for main heading
        if not re.search(r'^#\s+.+', content, re.MULTILINE):
            self.errors.append(f"{path.name}: Missing main heading (# Title)")
        
        # Check for overview/description
        if 'overview' not in content.lower() and 'description' not in content.lower():
            self.warnings.append(f"{path.name}: Missing Overview/Description section")
        
        # Check for rules section
        if 'rule' not in content.lower():
            self.warnings.append(f"{path.name}: No RULE sections found")
    
    def _check_code_examples(self, content: str, path: Path):
        """Validate code examples"""
        # Find all code blocks
        code_blocks = re.findall(r'```(\w+)?\n(.*?)```', content, re.DOTALL)
        
        for lang, code in code_blocks:
            # Check for common syntax errors
            if lang in ['javascript', 'typescript', 'js', 'ts']:
                self._validate_js_syntax(code, path)
            elif lang in ['python', 'py']:
                self._validate_python_syntax(code, path)
    
    def _validate_js_syntax(self, code: str, path: Path):
        """Basic JS/TS syntax validation"""
        # Check for unmatched braces
        open_braces = code.count('{')
        close_braces = code.count('}')
        if open_braces != close_braces:
            self.errors.append(f"{path.name}: Unmatched braces in JS code example")
        
        # Check for unmatched parentheses
        open_parens = code.count('(')
        close_parens = code.count(')')
        if open_parens != close_parens:
            self.errors.append(f"{path.name}: Unmatched parentheses in JS code example")
    
    def _validate_python_syntax(self, code: str, path: Path):
        """Basic Python syntax validation"""
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            self.errors.append(f"{path.name}: Python syntax error: {e}")
    
    def _check_links(self, content: str, path: Path):
        """Check internal links"""
        # Find markdown links
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        
        for text, url in links:
            # Check internal file links
            if not url.startswith('http') and not url.startswith('#'):
                link_path = path.parent / url
                if not link_path.exists():
                    self.errors.append(f"{path.name}: Broken link: {url}")
    
    def _check_rules_format(self, content: str, path: Path):
        """Check RULE formatting consistency"""
        # Find all RULE declarations
        rules = re.findall(r'\*\*RULE[- ](\d+)\.\*\*', content)
        
        if rules:
            # Check sequential numbering
            rule_nums = [int(r) for r in rules]
            expected = list(range(1, len(rule_nums) + 1))
            if rule_nums != expected:
                self.warnings.append(f"{path.name}: Non-sequential rule numbering: {rule_nums}")


class SkillSystemValidator:
    """Validates the entire skills system"""
    
    def __init__(self):
        self.validator = SkillValidator()
        self.results = {
            'total_skills': 0,
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'errors': []
        }
    
    def validate_all_skills(self) -> Dict:
        """Validate all skill files"""
        print("🔍 Scanning skills directory...")
        
        skill_files = list(SKILLS_ROOT.rglob('*.md'))
        self.results['total_skills'] = len(skill_files)
        
        print(f"📊 Found {len(skill_files)} skill files\n")
        
        for skill_file in skill_files:
            passed, errors, warnings = self.validator.validate_skill_file(skill_file)
            
            if passed:
                self.results['passed'] += 1
                print(f"✅ {skill_file.relative_to(SKILLS_ROOT)}")
            else:
                self.results['failed'] += 1
                print(f"❌ {skill_file.relative_to(SKILLS_ROOT)}")
                for error in errors:
                    print(f"   ERROR: {error}")
                    self.results['errors'].append(error)
            
            if warnings:
                self.results['warnings'] += len(warnings)
                for warning in warnings:
                    print(f"   ⚠️  {warning}")
        
        return self.results
    
    def check_master_router_consistency(self) -> List[str]:
        """Check MASTER_ROUTER.md references valid skills"""
        errors = []
        
        router_path = SKILLS_ROOT / "MASTER_ROUTER.md"
        if not router_path.exists():
            errors.append("MASTER_ROUTER.md not found")
            return errors
        
        content = router_path.read_text(encoding='utf-8')
        
        # Find all skill references
        skill_refs = re.findall(r'`([^`]+\.md)`', content)
        
        for ref in skill_refs:
            skill_path = SKILLS_ROOT / ref
            if not skill_path.exists():
                errors.append(f"MASTER_ROUTER references non-existent skill: {ref}")
        
        return errors
    
    def check_kiro_rules_consistency(self) -> List[str]:
        """Check KIRO.md rules reference valid skills"""
        errors = []
        
        if not KIRO_RULES.exists():
            errors.append("KIRO.md not found")
            return errors
        
        content = KIRO_RULES.read_text(encoding='utf-8')
        
        # Find all skill references
        skill_refs = re.findall(r'antigravity/skills/([^\s\)]+\.md)', content)
        
        for ref in skill_refs:
            skill_path = SKILLS_ROOT / ref
            if not skill_path.exists():
                errors.append(f"KIRO.md references non-existent skill: {ref}")
        
        return errors
    
    def generate_report(self):
        """Generate validation report"""
        print("\n" + "="*60)
        print("📊 SKILLS VALIDATION REPORT")
        print("="*60)
        
        print(f"\n📈 Statistics:")
        print(f"   Total Skills: {self.results['total_skills']}")
        print(f"   ✅ Passed: {self.results['passed']}")
        print(f"   ❌ Failed: {self.results['failed']}")
        print(f"   ⚠️  Warnings: {self.results['warnings']}")
        
        # Check system consistency
        print(f"\n🔗 System Consistency:")
        router_errors = self.check_master_router_consistency()
        if router_errors:
            print(f"   ❌ MASTER_ROUTER issues: {len(router_errors)}")
            for error in router_errors:
                print(f"      - {error}")
        else:
            print(f"   ✅ MASTER_ROUTER consistent")
        
        kiro_errors = self.check_kiro_rules_consistency()
        if kiro_errors:
            print(f"   ❌ KIRO.md issues: {len(kiro_errors)}")
            for error in kiro_errors:
                print(f"      - {error}")
        else:
            print(f"   ✅ KIRO.md consistent")
        
        # Overall status
        print(f"\n🎯 Overall Status:")
        if self.results['failed'] == 0 and not router_errors and not kiro_errors:
            print("   ✅ ALL CHECKS PASSED")
            return 0
        else:
            print("   ❌ VALIDATION FAILED")
            return 1


def main():
    """Main entry point"""
    print("🚀 Starting Skills System Validation\n")
    
    validator = SkillSystemValidator()
    validator.validate_all_skills()
    exit_code = validator.generate_report()
    
    return exit_code


if __name__ == "__main__":
    exit(main())
