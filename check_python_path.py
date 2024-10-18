import sys
import os

print("Python path:")
for path in sys.path:
    print(path)

print("\nContent of genesys/__init__.py:")
with open('genesys/__init__.py', 'r') as f:
    print(f.read())

print("\nContent of genesys/tools/__init__.py:")
with open('genesys/tools/__init__.py', 'r') as f:
    print(f.read())

print("\nProject structure:")
for root, dirs, files in os.walk('.'):
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 4 * level
    print(f"{indent}{os.path.basename(root)}/")
    sub_indent = ' ' * 4 * (level + 1)
    for file in files:
        print(f"{sub_indent}{file}")
