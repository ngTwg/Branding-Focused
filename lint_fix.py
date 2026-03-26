
import os

root_path = r"c:\Users\lengo\RPGITHUB"
md_files = []
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith(".md"):
            md_files.append(os.path.join(root, file))

fixed_count = 0

for file_path in md_files:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            # 1. Replace hard tabs with 4 spaces
            line = line.replace("\t", "    ")
            # 2. Remove trailing whitespace
            line = line.rstrip() + "\n"
            new_lines.append(line)
        
        # 3. Ensure single blank line at EOF
        if new_lines:
            content = "".join(new_lines).strip() + "\n"
        else:
            content = ""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        fixed_count += 1
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")

print(f"Fixed {fixed_count} markdown files.")
