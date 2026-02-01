#!/usr/bin/env python3
"""
PreToolUse hook for Write tool: validates SKILL.md files.
Checks:
- Max 500 lines
- Must have frontmatter with name and description
- Description must be in English (no Korean)
- No ## Overview or ## Activation sections (redundant)
"""

import json
import re
import sys


def check_skill_quality(file_path: str, content: str) -> list[str]:
    """Validate a SKILL.md file and return list of issues."""
    issues = []

    lines = content.split("\n")

    # Check max lines
    if len(lines) > 500:
        issues.append(f"File exceeds 500 lines ({len(lines)} lines). Consider compression.")

    # Check frontmatter
    if not content.startswith("---"):
        issues.append("Missing frontmatter (must start with ---)")
        return issues

    # Find frontmatter end
    second_delimiter = content.find("---", 3)
    if second_delimiter == -1:
        issues.append("Malformed frontmatter (missing closing ---)")
        return issues

    frontmatter = content[3:second_delimiter]

    # Check required fields
    has_name = bool(re.search(r"^name:\s*.+", frontmatter, re.MULTILINE))
    has_description = bool(re.search(r"^description:\s*.+", frontmatter, re.MULTILINE))

    if not has_name:
        issues.append("Frontmatter missing 'name' field")
    if not has_description:
        issues.append("Frontmatter missing 'description' field")

    # Check description is in English (no Korean characters)
    description_match = re.search(r"^description:\s*(.+)", frontmatter, re.MULTILINE)
    if description_match:
        description = description_match.group(1)
        korean_pattern = re.compile(r"[\uac00-\ud7af\u1100-\u11ff\u3130-\u318f\ua960-\ua97f\ud7b0-\ud7ff]")
        if korean_pattern.search(description):
            issues.append("Description contains Korean text (should be English)")

    # Check for redundant sections
    body = content[second_delimiter + 3:]
    if re.search(r"^##\s+Overview", body, re.MULTILINE):
        issues.append("Contains '## Overview' section (redundant with frontmatter description)")
    if re.search(r"^##\s+Activation", body, re.MULTILINE):
        issues.append("Contains '## Activation' section (redundant with frontmatter description)")

    return issues


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_input = input_data.get("tool_input", {})

        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")

        # Only check SKILL.md files
        if not file_path.endswith("SKILL.md"):
            sys.exit(0)

        issues = check_skill_quality(file_path, content)

        if not issues:
            sys.exit(0)

        # Report issues as warning (allow but inform)
        issues_text = "\n".join(f"  - {issue}" for issue in issues)
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
            },
            "systemMessage": f"SKILL.md quality check for {file_path}:\n{issues_text}\n\nConsider fixing these issues for better skill quality."
        }
        print(json.dumps(output))
        sys.exit(0)

    except Exception as e:
        # On error, allow the operation to proceed
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
