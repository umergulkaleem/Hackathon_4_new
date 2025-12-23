#!/usr/bin/env python3
"""
Script to test documentation content for proper structure and accessibility.
"""

import os
import re
from pathlib import Path

def check_frontmatter(filepath):
    """Check if markdown file has proper frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file starts with frontmatter
    if content.strip().startswith('---'):
        # Find the end of frontmatter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            # Check for required fields
            has_sidebar_label = 'sidebar_label:' in frontmatter
            has_sidebar_position = 'sidebar_position:' in frontmatter
            return has_sidebar_label and has_sidebar_position
    return True  # Files without frontmatter are still valid

def check_headings(filepath):
    """Check if markdown file has proper heading structure."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all headings
    headings = re.findall(r'^#+\s+(.*)', content, re.MULTILINE)

    # Check if there's at least one main heading
    main_headings = [h for h in headings if not h.startswith('#')]
    return len(main_headings) > 0

def check_alt_text(filepath):
    """Check if markdown file has alt text for images."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find image references
    images = re.findall(r'!\[([^\]]*)\]\([^)]+\)', content)

    # Check if all images have alt text (non-empty alt text)
    for alt_text in images:
        if not alt_text.strip():
            return False
    return True

def find_markdown_files(directory):
    """Find all markdown files in the docs directory."""
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                markdown_files.append(Path(root) / file)
    return markdown_files

def main():
    # Define the docs directory path
    docs_dir = Path("docs")

    if not docs_dir.exists():
        print(f"Error: Directory {docs_dir} does not exist")
        return 1

    # Find all markdown files
    markdown_files = find_markdown_files(docs_dir)

    if not markdown_files:
        print(f"No markdown files found in {docs_dir}")
        return 1

    print(f"Testing {len(markdown_files)} markdown files for proper structure...\n")

    # Test each markdown file
    all_passed = True
    for md_file in markdown_files:
        print(f"Testing {md_file}...")

        # Check frontmatter
        has_frontmatter = check_frontmatter(md_file)
        if not has_frontmatter:
            print(f"  [FAIL] Missing required frontmatter fields in {md_file.name}")
            all_passed = False
        else:
            print(f"  [PASS] Frontmatter check passed")

        # Check headings
        has_headings = check_headings(md_file)
        if not has_headings:
            print(f"  [FAIL] Missing main heading in {md_file.name}")
            all_passed = False
        else:
            print(f"  [PASS] Heading structure check passed")

        # Check alt text for images
        has_alt_text = check_alt_text(md_file)
        if not has_alt_text:
            print(f"  [FAIL] Missing alt text for images in {md_file.name}")
            all_passed = False
        else:
            print(f"  [PASS] Alt text check passed")

        print()

    print(f"Documentation testing complete.")
    if all_passed:
        print("[SUCCESS] All documentation content passed tests.")
        return 0
    else:
        print("[FAILURE] Some documentation content failed tests.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())