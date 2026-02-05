import os

file_path = r'frontend-react\src\components\moderation\ModerationAlert.js'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the malformed import
content = content.replace('import {`n  Box,`n  Dialog,', 'import {\n  Box,\n  Dialog,')

# Also ensure Box is properly added if not already there
if 'Box,' not in content:
    content = content.replace(
        'import {\n  Dialog,',
        'import {\n  Box,\n  Dialog,'
    )

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Fixed ModerationAlert.js - Added Box import')
