#!/usr/bin/env python3
"""
Git commit 성공 후 Slack 알림을 보내는 PostToolUse hook
- git commit 명령어가 성공적으로 실행되었을 때만 알림 전송
- SLACK_WEBHOOK_URL 환경 변수 필요
"""

import json
import os
import subprocess
import sys
from datetime import datetime


def get_last_commit_info():
    """마지막 커밋 정보 반환"""
    try:
        # 커밋 해시
        hash_result = subprocess.run(
            ["git", "log", "-1", "--format=%h"],
            capture_output=True,
            text=True
        )
        commit_hash = hash_result.stdout.strip()

        # 커밋 메시지
        msg_result = subprocess.run(
            ["git", "log", "-1", "--format=%s"],
            capture_output=True,
            text=True
        )
        commit_msg = msg_result.stdout.strip()

        # 변경된 파일 목록
        files_result = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
            capture_output=True,
            text=True
        )
        changed_files = files_result.stdout.strip().split("\n") if files_result.stdout.strip() else []

        # 브랜치 이름
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True
        )
        branch = branch_result.stdout.strip()

        return {
            "hash": commit_hash,
            "message": commit_msg,
            "files": changed_files,
            "branch": branch
        }
    except Exception:
        return None


def send_slack_notification(commit_info):
    """Slack으로 알림 전송"""
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return False

    # 변경된 파일 포맷팅 (최대 10개)
    files = commit_info["files"][:10]
    files_text = ", ".join([f"`{f}`" for f in files])
    if len(commit_info["files"]) > 10:
        files_text += f" 외 {len(commit_info['files']) - 10}개"

    # 현재 시간
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Git Commit 완료",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Branch:*\n`{commit_info['branch']}`"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Commit:*\n`{commit_info['hash']}`"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Message:*\n{commit_info['message']}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Changed Files ({len(commit_info['files'])}):*\n{files_text}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Claude Code | {now}"
                    }
                ]
            }
        ]
    }

    try:
        result = subprocess.run(
            [
                "curl", "-s", "-X", "POST",
                "-H", "Content-type: application/json",
                "--data", json.dumps(payload),
                webhook_url
            ],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def main():
    try:
        input_data = json.load(sys.stdin)

        tool_input = input_data.get("tool_input", {})
        tool_result = input_data.get("tool_result", {})

        command = tool_input.get("command", "")
        stdout = tool_result.get("stdout", "")
        stderr = tool_result.get("stderr", "")

        # git commit 명령어인지 확인
        if "git commit" not in command:
            sys.exit(0)

        # 커밋 실패 시 무시 (에러 메시지 확인)
        error_indicators = [
            "nothing to commit",
            "error:",
            "fatal:",
            "Aborting commit",
            "pre-commit hook",
            "hook failed"
        ]

        combined_output = stdout + stderr
        for indicator in error_indicators:
            if indicator.lower() in combined_output.lower():
                sys.exit(0)

        # 커밋 성공 시 알림 전송
        commit_info = get_last_commit_info()
        if commit_info:
            success = send_slack_notification(commit_info)
            if success:
                output = {
                    "systemMessage": f"Slack 알림 전송 완료: {commit_info['hash']} - {commit_info['message'][:50]}"
                }
                print(json.dumps(output))

        sys.exit(0)

    except Exception as e:
        # 에러 시에도 통과 (안전)
        sys.exit(0)


if __name__ == "__main__":
    main()
