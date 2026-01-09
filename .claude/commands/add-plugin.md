# Add Plugin Command

> 마켓플레이스에 새 플러그인을 추가합니다

## 사용법

```
/add-plugin <plugin-name>
```

$ARGUMENTS 로 플러그인 이름이 전달됩니다.

## 워크플로우

### 1. 플러그인 정보 수집

사용자에게 질문:
- 플러그인 이름 (kebab-case)
- 플러그인 설명
- 카테고리 (development, productivity, utilities 등)
- 키워드

### 2. 디렉토리 구조 생성

```bash
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
├── skills/
├── agents/
├── commands/
└── hooks/
```

### 3. plugin.json 생성

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "<플러그인 설명>",
  "author": {
    "name": "ddingg"
  },
  "keywords": ["<keyword1>", "<keyword2>"],
  "category": "<category>"
}
```

### 4. marketplace.json 업데이트

`.claude-plugin/marketplace.json`의 plugins 배열에 추가:

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "<플러그인 설명>",
  "version": "1.0.0",
  "category": "<category>",
  "keywords": ["<keyword1>", "<keyword2>"]
}
```

### 5. README.md 업데이트 안내

플러그인 추가 후 README.md에 새 플러그인 정보를 추가해야 합니다.

## 네이밍 컨벤션

- 플러그인 이름: `kebab-case`
- 디렉토리: `plugins/<plugin-name>/`
- 매니페스트: `.claude-plugin/plugin.json`

## 예시

```
/add-plugin backend-tools
```

결과:
```
plugins/backend-tools/
├── .claude-plugin/
│   └── plugin.json
├── skills/
├── agents/
├── commands/
└── hooks/
```

## 주의사항

- 플러그인 이름은 마켓플레이스 내에서 고유해야 합니다
- 플러그인 이름에는 공백이나 특수문자를 사용할 수 없습니다
- 플러그인 추가 후 반드시 marketplace.json을 업데이트해야 합니다
