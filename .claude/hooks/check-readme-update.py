#!/usr/bin/env python3
"""
Commit 전 README 업데이트 필요 여부 체크
- plugins/ 또는 .claude-plugin/ 변경 시 README.md도 함께 업데이트 필요
"""

import json
import subprocess
import sys

def get_staged_files():
    """스테이징된 파일 목록 반환"""
    result = subprocess.run(
        ["git", "diff", "--staged", "--name-only"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split("\n") if result.stdout.strip() else []

def needs_readme_update(staged_files):
    """README 업데이트가 필요한지 판단"""
    # README 업데이트가 필요한 파일 패턴
    trigger_patterns = [
        "plugins/",
        ".claude-plugin/marketplace.json",
    ]

    has_trigger_changes = False
    has_readme_changes = False

    for file in staged_files:
        # README 변경 여부
        if file == "README.md":
            has_readme_changes = True

        # 트리거 파일 변경 여부
        for pattern in trigger_patterns:
            if file.startswith(pattern) or file == pattern:
                has_trigger_changes = True
                break

    return has_trigger_changes and not has_readme_changes

def main():
    try:
        input_data = json.load(sys.stdin)
        command = input_data.get("tool_input", {}).get("command", "")

        # git commit 명령어가 아니면 통과
        if "git commit" not in command:
            sys.exit(0)

        staged_files = get_staged_files()

        if needs_readme_update(staged_files):
            # 변경된 plugin 파일 목록
            changed_plugins = [f for f in staged_files if f.startswith("plugins/")]
            changed_marketplace = [f for f in staged_files if ".claude-plugin" in f]

            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "README.md 업데이트가 필요합니다"
                },
                "systemMessage": f"""⚠️ README.md 업데이트 필요

변경된 파일:
- {chr(10).join(changed_plugins + changed_marketplace)}

README.md에 새로운 플러그인/변경사항을 반영해주세요.
업데이트 후 다시 commit을 시도하세요."""
            }
            print(json.dumps(output))
            sys.exit(0)

        # README 업데이트 불필요하면 통과
        sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)  # 에러 시에도 통과 (안전)

if __name__ == "__main__":
    main()
