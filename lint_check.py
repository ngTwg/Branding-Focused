
import os
import re

root_path = r"c:\Users\lengo\RPGITHUB"
md_files = []
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith(".md"):
            md_files.append(os.path.join(root, file))

issues = []

for file_path in md_files:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines):
            # Trailing whitespace
            if line.endswith(" \n") or line.endswith("\t\n"):
                issues.append(f"{file_path}:{i+1}: Trailing whitespace")
            
            # MD001 Heading levels should only increment by one
            # (Simple check)
            
            # MD010 Hard tabs
            if "\t" in line:
                issues.append(f"{file_path}:{i+1}: Hard tabs detected")
            
            # MD009 Trailing spaces
            
        # MD047 Final newline
        if lines and not lines[-1].endswith("\n"):
            issues.append(f"{file_path}:{len(lines)}: No newline at end of file")

    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Output top issues
with open(os.path.join(root_path, "lint_report.txt"), "w", encoding="utf-8") as f:
    for issue in issues:
        f.write(issue + "\n")

print(f"Found {len(issues)} potential lint issues. Saved to lint_report.txt")
