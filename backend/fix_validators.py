"""
Script to fix Pydantic V1 validators to V2 field_validators
"""
import re
import os

files_to_fix = [
    'app/api/nodes.py',
    'app/api/elements.py',
    'app/api/materials.py',
    'app/api/sections.py',
    'app/api/loads.py',
    'app/api/analysis.py',
]

for filepath in files_to_fix:
    full_path = os.path.join(os.path.dirname(__file__), filepath)
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace imports
    content = content.replace(
        'from pydantic import BaseModel, validator, Field',
        'from pydantic import BaseModel, field_validator, Field'
    )
    content = content.replace(
        'from pydantic import BaseModel, validator',
        'from pydantic import BaseModel, field_validator'
    )
    
    # Replace @validator with @field_validator and add @classmethod
    # Pattern: @validator(...)\n    def method_name(cls, v, ...):
    pattern = r'@validator\((.*?)\)\s+def\s+(\w+)\(cls,\s*v(?:,\s*(?:field|values|info))?\):'
    
    def replace_validator(match):
        args = match.group(1)
        method_name = match.group(2)
        return f'@field_validator({args})\n    @classmethod\n    def {method_name}(cls, v, info):'
    
    content = re.sub(pattern, replace_validator, content)
    
    # Replace field.name with info.field_name
    content = content.replace('field.name', 'info.field_name')
    
    # Replace values with info (for cross-field validation)
    # This is a simplified replacement - may need manual review
    content = re.sub(r'values\[([\'"])(.*?)\1\]', r'info.data.get(\1\2\1)', content)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {filepath}")

print("\nAll files fixed! Please review the changes.")
