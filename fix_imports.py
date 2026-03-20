import os
import re
import glob

ui_dir = os.path.join("src", "components", "ui")
files = glob.glob(os.path.join(ui_dir, "*.tsx"))

pattern = re.compile(r'(from\s+["\'][^"\']+?)@[0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9.]+)?(["\'])')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, num_subs = pattern.subn(r'\1\2', content)
    
    if num_subs > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {num_subs} imports in {filepath}")

print("Done.")
