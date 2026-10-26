#!/usr/bin/env python3
"""
Verification script for HTML pages in the Corporate Governance & Agent Architecture website.
Ensures:
1. Every HTML file contains the Google tag (gtag.js) with ID G-Z56XV344LR immediately after <head>.
2. No page has more than one Google tag.
3. All HTML tags are properly balanced.
"""

import glob
import os
import re
import sys
from html.parser import HTMLParser

EXPECTED_TAG_SNIPPET = "https://www.googletagmanager.com/gtag/js?id=G-Z56XV344LR"
EXPECTED_CONFIG_CALL = "gtag('config', 'G-Z56XV344LR');"

class TagValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.void_tags = {
            "area", "base", "br", "col", "embed", "hr",
            "img", "input", "link", "meta", "param",
            "source", "track", "wbr"
        }
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.void_tags:
            self.stack.append((tag.lower(), self.getpos()))

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower in self.void_tags:
            return
        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{tag}> at line {self.getpos()[0]}")
            return
        last_tag, pos = self.stack.pop()
        if last_tag != tag_lower:
            self.errors.append(
                f"Mismatched tag: opened <{last_tag}> at line {pos[0]} closed by </{tag}> at line {self.getpos()[0]}"
            )

def verify_file(filepath):
    errors = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check head tag existence
    head_match = re.search(r"<head[^>]*>", content, re.IGNORECASE)
    if not head_match:
        errors.append("Missing <head> element")
        return errors

    # 2. Check Google tag presence immediately after <head>
    after_head = content[head_match.end():].lstrip()
    if not after_head.startswith("<!-- Google tag (gtag.js) -->"):
        errors.append("Google tag (gtag.js) is NOT placed immediately after <head>")

    # 3. Check for exact single inclusion
    script_count = content.count(EXPECTED_TAG_SNIPPET)
    config_count = content.count(EXPECTED_CONFIG_CALL)

    if script_count == 0:
        errors.append("Missing Google tag script (G-Z56XV344LR)")
    elif script_count > 1:
        errors.append(f"Duplicate Google tag script found ({script_count} occurrences)")

    if config_count == 0:
        errors.append("Missing gtag config call for G-Z56XV344LR")
    elif config_count > 1:
        errors.append(f"Duplicate gtag config call found ({config_count} occurrences)")

    # 4. Check HTML structure balance
    validator = TagValidator()
    validator.feed(content)
    if validator.errors:
        errors.extend(validator.errors)
    if validator.stack:
        unclosed = [tag for tag, _ in validator.stack]
        errors.append(f"Unclosed tags at end of file: {unclosed}")

    return errors

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_files = sorted(glob.glob(os.path.join(root_dir, "**/*.html"), recursive=True))

    total_errors = 0
    print(f"Checking {len(html_files)} HTML files for Google tag and HTML integrity...")

    for path in html_files:
        rel_path = os.path.relpath(path, root_dir)
        errors = verify_file(path)
        if errors:
            total_errors += len(errors)
            print(f"FAIL: {rel_path}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"OK:   {rel_path}")

    if total_errors > 0:
        print(f"\nVerification FAILED: {total_errors} issue(s) detected.")
        sys.exit(1)
    else:
        print(f"\nAll {len(html_files)} HTML files passed verification successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
