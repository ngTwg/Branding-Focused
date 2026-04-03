#!/usr/bin/env python3
"""
Auto Training Pipeline
Extract [Error + Fix] pairs from conversations → JSONL for Ollama training

Features:
- Extract error-fix pairs from conversation logs
- Auto-trigger message when dataset > 500 samples
- Generate Modelfile for Ollama
- Support multiple conversation formats
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime


# Configuration
CONV_DIR = Path("C:/Users/<YOUR_USERNAME>/.gemini/antigravity/conversations")
OUTPUT_DIR = Path("C:/Users/<YOUR_USERNAME>/.gemini/antigravity/training_data")
OUTPUT_FILE = OUTPUT_DIR / "auto_extracted.jsonl"
MODELFILE = OUTPUT_DIR / "Modelfile"
THRESHOLD = 500  # Auto-trigger threshold


class ConversationParser:
    """Parse conversations to extract error-fix pairs"""
    
    # Patterns to detect errors
    ERROR_PATTERNS = [
        r'ERROR[:\s]+(.+?)(?=FIX:|SOLUTION:|FIXED:|$)',
        r'BUG[:\s]+(.+?)(?=FIX:|SOLUTION:|FIXED:|$)',
        r'ISSUE[:\s]+(.+?)(?=FIX:|SOLUTION:|FIXED:|$)',
        r'PROBLEM[:\s]+(.+?)(?=FIX:|SOLUTION:|FIXED:|$)',
        r'❌[:\s]+(.+?)(?=✅|FIX:|SOLUTION:|$)',
    ]
    
    # Patterns to detect fixes
    FIX_PATTERNS = [
        r'(?:FIX|SOLUTION|FIXED)[:\s]+(.+?)(?=ERROR:|BUG:|ISSUE:|$)',
        r'✅[:\s]+(.+?)(?=❌|ERROR:|BUG:|$)',
        r'RESOLVED[:\s]+(.+?)(?=ERROR:|BUG:|$)',
    ]
    
    def extract_pairs(self, text: str) -> List[Dict[str, str]]:
        """
        Extract error-fix pairs from text
        
        Args:
            text: Conversation text
        
        Returns:
            List of {prompt, response} dicts
        """
        pairs = []
        
        # Find all errors
        errors = []
        for pattern in self.ERROR_PATTERNS:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                error_text = match.group(1).strip()
                if len(error_text) > 10:  # Filter out too short
                    errors.append(error_text)
        
        # Find all fixes
        fixes = []
        for pattern in self.FIX_PATTERNS:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                fix_text = match.group(1).strip()
                if len(fix_text) > 10:  # Filter out too short
                    fixes.append(fix_text)
        
        # Pair errors with fixes
        for error, fix in zip(errors, fixes):
            # Truncate to reasonable length
            error_truncated = error[:400]
            fix_truncated = fix[:800]
            
            pairs.append({
                "prompt": f"Fix this error: {error_truncated}",
                "response": fix_truncated
            })
        
        return pairs
    
    def extract_from_code_blocks(self, text: str) -> List[Dict[str, str]]:
        """
        Extract before/after code pairs
        
        Args:
            text: Conversation text with code blocks
        
        Returns:
            List of {prompt, response} dicts
        """
        pairs = []
        
        # Find code blocks with "before" and "after" labels
        before_pattern = r'(?:BEFORE|OLD|BROKEN)[:\s]*```[\w]*\n(.+?)```'
        after_pattern = r'(?:AFTER|NEW|FIXED)[:\s]*```[\w]*\n(.+?)```'
        
        befores = re.finditer(before_pattern, text, re.DOTALL | re.IGNORECASE)
        afters = re.finditer(after_pattern, text, re.DOTALL | re.IGNORECASE)
        
        before_list = [m.group(1).strip() for m in befores]
        after_list = [m.group(1).strip() for m in afters]
        
        for before, after in zip(before_list, after_list):
            if len(before) > 20 and len(after) > 20:
                pairs.append({
                    "prompt": f"Refactor this code:\n```\n{before[:500]}\n```",
                    "response": f"```\n{after[:800]}\n```"
                })
        
        return pairs


class TrainingDataExtractor:
    """Main extractor class"""
    
    def __init__(self, conv_dir: Path, output_file: Path):
        self.conv_dir = conv_dir
        self.output_file = output_file
        self.parser = ConversationParser()
    
    def scan_conversations(self) -> List[Path]:
        """Scan conversation directory for text files"""
        if not self.conv_dir.exists():
            print(f"⚠️ Conversation directory not found: {self.conv_dir}")
            return []
        
        # Find all .txt, .md, .log files
        files = []
        for ext in ["*.txt", "*.md", "*.log"]:
            files.extend(self.conv_dir.rglob(ext))
        
        return files
    
    def extract_all(self) -> List[Dict[str, str]]:
        """
        Extract training pairs from all conversations
        
        Returns:
            List of {prompt, response} dicts
        """
        print("🔍 Scanning conversations...")
        files = self.scan_conversations()
        print(f"   Found {len(files)} conversation files")
        
        all_pairs = []
        
        for file_path in files:
            try:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
                
                # Extract error-fix pairs
                pairs = self.parser.extract_pairs(text)
                all_pairs.extend(pairs)
                
                # Extract code refactoring pairs
                code_pairs = self.parser.extract_from_code_blocks(text)
                all_pairs.extend(code_pairs)
                
                if pairs or code_pairs:
                    print(f"   ✅ {file_path.name}: {len(pairs)} error-fix, {len(code_pairs)} code pairs")
            
            except Exception as e:
                print(f"   ⚠️ Error reading {file_path.name}: {e}")
        
        return all_pairs
    
    def save_jsonl(self, pairs: List[Dict[str, str]]) -> int:
        """
        Save pairs to JSONL file
        
        Args:
            pairs: List of {prompt, response} dicts
        
        Returns:
            Number of pairs saved
        """
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for pair in pairs:
                json_line = json.dumps(pair, ensure_ascii=False)
                f.write(json_line + '\n')
        
        return len(pairs)
    
    def generate_modelfile(self, base_model: str = "llama3.2"):
        """
        Generate Modelfile for Ollama
        
        Args:
            base_model: Base model to use (default: llama3.2)
        """
        modelfile_content = f"""# Antigravity Custom Model
# Generated: {datetime.now().isoformat()}

FROM {base_model}

# System prompt
SYSTEM \"\"\"
You are an expert AI assistant specialized in debugging and fixing code.
You have been trained on real error-fix pairs from the Antigravity project.

Your expertise includes:
- Systematic debugging (no guess-and-check)
- Root cause analysis
- Security-first coding (OWASP)
- Anti-hallucination (verify before suggesting)
- Best practices for React, Node.js, Python, TypeScript

Always:
1. Analyze the root cause first
2. Suggest specific, actionable fixes
3. Verify library/API existence before recommending
4. Follow naming conventions
5. Add proper error handling
\"\"\"

# Parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40

# Training data
ADAPTER {self.output_file.name}
"""
        
        MODELFILE.write_text(modelfile_content, encoding='utf-8')
        print(f"✅ Modelfile generated: {MODELFILE}")
    
    def run(self) -> Dict:
        """
        Run full extraction pipeline
        
        Returns:
            Dict with results
        """
        print("🚀 Auto Training Pipeline")
        print(f"   Conversations: {self.conv_dir}")
        print(f"   Output: {self.output_file}")
        print()
        
        # Extract pairs
        pairs = self.extract_all()
        
        # Remove duplicates
        unique_pairs = []
        seen = set()
        for pair in pairs:
            key = (pair["prompt"][:100], pair["response"][:100])
            if key not in seen:
                seen.add(key)
                unique_pairs.append(pair)
        
        print()
        print(f"📊 Extraction Results:")
        print(f"   Total pairs: {len(pairs)}")
        print(f"   Unique pairs: {len(unique_pairs)}")
        
        # Save to JSONL
        saved = self.save_jsonl(unique_pairs)
        print(f"   Saved: {saved} pairs → {self.output_file}")
        
        # Generate Modelfile
        self.generate_modelfile()
        
        # Check threshold
        if len(unique_pairs) >= THRESHOLD:
            print()
            print("🚀 " + "="*60)
            print(f"   READY FOR TRAINING! Dataset has {len(unique_pairs)} samples (≥{THRESHOLD})")
            print("   " + "="*60)
            print()
            print("   Next steps:")
            print(f"   1. cd {OUTPUT_DIR}")
            print("   2. ollama create ngtwg-custom -f Modelfile")
            print("   3. ollama run ngtwg-custom")
            print()
        else:
            remaining = THRESHOLD - len(unique_pairs)
            print()
            print(f"ℹ️ Need {remaining} more samples to reach threshold ({THRESHOLD})")
        
        return {
            "total_pairs": len(pairs),
            "unique_pairs": len(unique_pairs),
            "saved": saved,
            "threshold": THRESHOLD,
            "ready": len(unique_pairs) >= THRESHOLD
        }


def main():
    """CLI entry point"""
    import sys
    
    # Parse arguments
    conv_dir = CONV_DIR
    output_file = OUTPUT_FILE
    
    if "--conv-dir" in sys.argv:
        idx = sys.argv.index("--conv-dir")
        conv_dir = Path(sys.argv[idx + 1])
    
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        output_file = Path(sys.argv[idx + 1])
    
    # Run extraction
    extractor = TrainingDataExtractor(conv_dir, output_file)
    results = extractor.run()
    
    # Exit code
    sys.exit(0 if results["saved"] > 0 else 1)


if __name__ == "__main__":
    main()
