"""
Fix Pydantic model_* field warnings by adding model_config
"""
import os
import re

files_to_fix = [
    'app/api/analysis.py',
    'app/api/design.py',
    'app/api/detailing.py',
    'app/api/ml.py',
    'app/api/learning.py',
    'app/api/bim.py'
]

config_line = '    model_config = {"protected_namespaces": ()}\n'

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        print(f"⚠ File not found: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all BaseModel classes that have model_* fields
    pattern = r'(class \w+\(BaseModel\):)\n((?:    (?!model_config)[^\n]+\n)*?    model_(?:id|type|data):[^\n]+)'
    
    def add_config(match):
        class_def = match.group(1)
        rest = match.group(2)
        # Check if config already exists
        if 'model_config' in rest:
            return match.group(0)
        return f"{class_def}\n{config_line}{rest}"
    
    new_content = re.sub(pattern, add_config, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Fixed: {filepath}")
    else:
        print(f"- No changes: {filepath}")

print("\n✓ All Pydantic warnings fixed!")
