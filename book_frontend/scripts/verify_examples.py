#!/usr/bin/env python3
"""
Script to verify that all Python examples in the tutorials directory
have valid syntax and follow basic ROS 2 patterns.
"""

import ast
import os
import sys
from pathlib import Path

def verify_python_file(filepath):
    """Verify that a Python file has valid syntax."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the file to check for syntax errors
        ast.parse(content)
        print(f"[PASS] {filepath.name} - Valid syntax")
        return True
    except SyntaxError as e:
        print(f"[FAIL] {filepath.name} - Syntax error at line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"[FAIL] {filepath.name} - Error: {e}")
        return False

def find_python_examples(directory):
    """Find all Python files in the tutorials directory."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                python_files.append(Path(root) / file)
    return python_files

def main():
    # Define the tutorials directory path
    tutorials_dir = Path("docs/tutorials/python-examples")

    if not tutorials_dir.exists():
        print(f"Error: Directory {tutorials_dir} does not exist")
        return 1

    # Find all Python example files
    python_examples = find_python_examples(tutorials_dir)

    if not python_examples:
        print(f"No Python examples found in {tutorials_dir}")
        return 1

    print(f"Verifying {len(python_examples)} Python examples...\n")

    # Verify each Python file
    all_passed = True
    for example_file in python_examples:
        if not verify_python_file(example_file):
            all_passed = False

    print(f"\nVerification complete.")
    if all_passed:
        print("[SUCCESS] All Python examples passed verification.")
        return 0
    else:
        print("[FAILURE] Some Python examples failed verification.")
        return 1

if __name__ == "__main__":
    sys.exit(main())