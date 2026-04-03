---
name: "File Organizer"
tags: ["antigravity", "c:", "count", "duplicates", "extension", "file", "files", "find", "frontend", "gemini", "identify", "large", "<YOUR_USERNAME>", "organizer", "overview", "rules", "specialized", "system", "tools", "users"]
tier: 2
risk: "medium"
estimated_tokens: 1802
tools_needed: ["git", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.93
---
# File Organizer

> **Tier:** 1-2  
> **Tags:** `files`, `organization`, `cleanup`, `duplicates`, `automation`  
> **When to use:** Organizing messy directories, removing duplicates, automating file management

---

## Overview

Intelligent file organization strategies for cleaning up downloads, removing duplicates, and maintaining logical folder structures. Includes automation scripts and best practices for file naming and categorization.

---

## Rules

**RULE-001: Analyze Before Acting**
Survey current structure before reorganizing. Identify patterns, duplicates, and logical groupings. Never delete or move files without understanding their purpose.

```bash
❌ Bad: Blind reorganization
mv * organized/  # Moves everything without analysis

✅ Good: Analyze first
# Count files by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Find large files
find . -type f -size +100M -exec ls -lh {} \;

# Identify duplicates
fdupes -r .
```

**RULE-002: Logical Grouping**
Group files by type, project, or date. Use consistent naming conventions. Create clear folder hierarchies (max 3-4 levels deep).

```bash
❌ Bad: Flat structure with unclear names
Downloads/
  file1.pdf
  document.docx
  image.jpg
  stuff.zip

✅ Good: Organized hierarchy
Documents/
  Work/
    Projects/
      ProjectA/
    Reports/
  Personal/
Media/
  Photos/
    2024/
  Videos/
Archives/
```

**RULE-003: Duplicate Detection**
Use hash-based comparison (MD5, SHA256) not just filename. Keep newest or highest quality version. Archive or delete duplicates safely.

```bash
# Find duplicates by content hash
fdupes -r -S /path/to/directory

# Find duplicates by size and name
find . -type f -exec md5sum {} + | sort | uniq -w32 -dD

# Python script for duplicate detection
import hashlib
from pathlib import Path

def find_duplicates(directory):
    hashes = {}
    for file in Path(directory).rglob('*'):
        if file.is_file():
            file_hash = hashlib.md5(file.read_bytes()).hexdigest()
            hashes.setdefault(file_hash, []).append(file)
    return {h: files for h, files in hashes.items() if len(files) > 1}
```

**RULE-004: Automated Cleanup**
Create scripts for recurring organization tasks. Schedule with cron (Unix) or Task Scheduler (Windows). Log all actions for audit trail.

```bash
❌ Bad: Manual cleanup every time
# Manually sort files each week

✅ Good: Automated script
#!/bin/bash
# organize_downloads.sh

DOWNLOADS="$HOME/Downloads"
DOCS="$HOME/Documents"
MEDIA="$HOME/Media"
ARCHIVES="$HOME/Archives"

# Move documents
find "$DOWNLOADS" -name "*.pdf" -mtime +7 -exec mv {} "$DOCS/" \;
find "$DOWNLOADS" -name "*.docx" -mtime +7 -exec mv {} "$DOCS/" \;

# Move media
find "$DOWNLOADS" -name "*.jpg" -mtime +7 -exec mv {} "$MEDIA/Photos/" \;
find "$DOWNLOADS" -name "*.mp4" -mtime +7 -exec mv {} "$MEDIA/Videos/" \;

# Archive old files
find "$DOWNLOADS" -name "*.zip" -mtime +30 -exec mv {} "$ARCHIVES/" \;

# Log actions
echo "$(date): Organized downloads" >> ~/organize.log
```

**RULE-005: Safe Deletion**
Move to trash/recycle bin instead of permanent deletion. Keep backups before bulk operations. Use dry-run mode to preview changes.

```bash
❌ Bad: Permanent deletion
rm -rf duplicates/  # No recovery possible

✅ Good: Safe deletion with trash
# macOS
brew install trash
trash duplicates/

# Linux
sudo apt install trash-cli
trash-put duplicates/

# Windows PowerShell
Move-Item duplicates/ $env:USERPROFILE\Recycle.Bin

# Dry-run mode (preview without executing)
find . -name "*.tmp" -print  # Preview
find . -name "*.tmp" -delete  # Execute after review
```

**RULE-006: Naming Conventions**
Use consistent, descriptive names. Include dates in ISO format (YYYY-MM-DD). Avoid spaces and special characters.

```bash
❌ Bad: Inconsistent naming
My Document (1).docx
final_FINAL_v2.pdf
IMG_1234.jpg

✅ Good: Consistent naming
2024-03-26_project-proposal.docx
2024-03-26_financial-report_v2.pdf
2024-03-26_team-photo.jpg

# Batch rename script
for file in *.jpg; do
  date=$(stat -f "%Sm" -t "%Y-%m-%d" "$file")
  mv "$file" "${date}_${file}"
done
```

**RULE-007: Metadata Preservation**
Preserve file timestamps, permissions, and extended attributes. Use appropriate copy/move commands. Document metadata in README files.

```bash
❌ Bad: Loses metadata
cp file.txt backup/  # Loses original timestamp

✅ Good: Preserves metadata
# Preserve timestamps
cp -p file.txt backup/

# Preserve all attributes
cp -a directory/ backup/

# rsync for complex operations
rsync -av --progress source/ destination/
```

**RULE-008: Context Maintenance**
Keep related files together. Create README files explaining folder contents. Use .gitkeep for empty folders in version control.

```markdown
# Project/README.md
## Folder Structure

- `src/` - Source code
- `docs/` - Documentation
- `tests/` - Test files
- `data/` - Data files (not in git)
- `output/` - Generated files (not in git)

## File Naming
- Source files: `module-name.ts`
- Test files: `module-name.test.ts`
- Data files: `YYYY-MM-DD_dataset-name.csv`
```

---

## Quick Reference

### File Organization Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| By Type | Mixed file types | `Documents/`, `Media/`, `Code/` |
| By Project | Project-based work | `ProjectA/`, `ProjectB/` |
| By Date | Time-series data | `2024/03/`, `2024/04/` |
| By Status | Workflow stages | `Inbox/`, `Processing/`, `Done/` |

### Duplicate Detection Tools

```bash
# fdupes (Unix)
fdupes -r -S directory/  # Recursive, show size

# rdfind (Unix)
rdfind -makehardlinks true directory/  # Replace with hardlinks

# PowerShell (Windows)
Get-ChildItem -Recurse | Group-Object -Property Length | Where-Object { $_.Count -gt 1 }

# Python (cross-platform)
pip install dupeguru
dupeguru  # GUI tool
```

### Automation Scripts

#### Daily Downloads Cleanup (Unix)
```bash
#!/bin/bash
# Add to crontab: 0 2 * * * /path/to/cleanup.sh

DOWNLOADS="$HOME/Downloads"
ARCHIVE="$HOME/Archive/$(date +%Y-%m)"

# Create archive folder
mkdir -p "$ARCHIVE"

# Move files older than 30 days
find "$DOWNLOADS" -type f -mtime +30 -exec mv {} "$ARCHIVE/" \;

# Remove empty folders
find "$DOWNLOADS" -type d -empty -delete
```

#### Weekly Duplicate Removal (Windows)
```powershell
# Add to Task Scheduler

$Downloads = "$env:USERPROFILE\Downloads"
$Duplicates = "$env:USERPROFILE\Duplicates"

# Find duplicates by hash
$files = Get-ChildItem -Path $Downloads -Recurse -File
$hashes = @{}

foreach ($file in $files) {
    $hash = Get-FileHash $file.FullName -Algorithm MD5
    if ($hashes.ContainsKey($hash.Hash)) {
        Move-Item $file.FullName $Duplicates
    } else {
        $hashes[$hash.Hash] = $file.FullName
    }
}
```

### Naming Convention Templates

```bash
# Documents
YYYY-MM-DD_document-title_vN.ext
2024-03-26_project-proposal_v1.docx

# Code
module-name.language
user-service.ts
user-service.test.ts

# Media
YYYY-MM-DD_description.ext
2024-03-26_team-meeting.jpg

# Data
YYYY-MM-DD_dataset-name.ext
2024-03-26_sales-data.csv
```

---

## Metadata

- **Related Skills:** [bash-linux.md], [powershell-windows.md], [automation-patterns.md]
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
