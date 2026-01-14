# Notify Slack Command

> 작업 완료 내용을 정리하여 Slack으로 알림을 보냅니다

## 사용법

```
/notify-slack [message]
```

$ARGUMENTS 로 추가 메시지가 전달될 수 있습니다.

## 환경 변수

- `SLACK_WEBHOOK_URL`: Slack Incoming Webhook URL (필수)

## 워크플로우

### 1. 작업 내용 수집

현재 대화에서 완료된 작업 내용을 분석하여 다음을 정리합니다:
- 완료된 주요 작업 목록
- 변경된 파일들
- 주요 변경 사항 요약

### 2. 메시지 포맷팅

Slack Block Kit 형식으로 포맷팅합니다:

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "작업 완료 알림",
        "emoji": true
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*완료된 작업:*\n- 작업 1\n- 작업 2"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*변경된 파일:*\n`file1.ts`, `file2.ts`"
      }
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Claude Code에서 전송됨"
        }
      ]
    }
  ]
}
```

### 3. Slack Webhook 전송

```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"blocks": [...]}' \
  "$SLACK_WEBHOOK_URL"
```

## 실행 지침

1. 먼저 `SLACK_WEBHOOK_URL` 환경 변수가 설정되어 있는지 확인합니다
2. 현재 대화에서 완료된 작업들을 분석합니다
3. 작업 내용을 Slack Block Kit 형식의 JSON으로 포맷팅합니다
4. curl 명령으로 `$SLACK_WEBHOOK_URL`에 POST 요청을 보냅니다
5. 전송 결과를 사용자에게 알립니다

## 메시지 구조

- **Header**: "작업 완료 알림" 또는 사용자 지정 제목
- **완료된 작업**: 불릿 포인트로 나열
- **변경된 파일**: 백틱으로 감싼 파일명 목록
- **추가 메시지**: $ARGUMENTS가 있으면 포함
- **Footer**: 타임스탬프 및 출처

## 예시

```
/notify-slack
```

결과: 현재 세션에서 완료된 작업 내용을 Slack으로 전송

```
/notify-slack PR #123 리뷰 완료
```

결과: 추가 메시지와 함께 작업 내용을 Slack으로 전송
