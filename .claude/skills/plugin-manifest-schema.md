# Plugin Manifest Schema

> Claude Code 플러그인의 plugin.json 스키마 가이드

## 활성화 조건

- plugin.json 파일 작성/수정 시
- 새 플러그인 생성 시
- `/add-plugin` 커맨드 실행 시

---

## 스키마 정의

### 필수 필드

| 필드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| `name` | string | 고유 식별자 (kebab-case, 공백 불가) | `"deployment-tools"` |

### 메타데이터 필드 (선택)

| 필드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| `version` | string | Semantic version | `"2.1.0"` |
| `description` | string | 플러그인 목적 설명 | `"Deployment automation tools"` |
| `author` | object | 작성자 정보 | `{"name": "Dev", "email": "dev@co.com"}` |
| `homepage` | string | 문서 URL | `"https://docs.example.com"` |
| `repository` | string | 소스 코드 URL | `"https://github.com/user/plugin"` |
| `license` | string | 라이센스 식별자 | `"MIT"`, `"Apache-2.0"` |
| `keywords` | array | 검색 태그 | `["deployment", "ci-cd"]` |

### 컴포넌트 경로 필드 (선택)

| 필드 | 타입 | 설명 | 예시 |
|------|------|------|------|
| `commands` | string \| array | 추가 커맨드 파일/디렉토리 | `"./custom/cmd.md"` |
| `agents` | string \| array | 추가 에이전트 파일 | `"./custom/agents/"` |
| `skills` | string \| array | 추가 스킬 디렉토리 | `"./custom/skills/"` |
| `hooks` | string \| object | Hook 설정 경로 또는 인라인 설정 | `"./hooks.json"` |
| `mcpServers` | string \| object | MCP 설정 경로 또는 인라인 설정 | `"./mcp-config.json"` |
| `outputStyles` | string \| array | 추가 출력 스타일 파일/디렉토리 | `"./styles/"` |
| `lspServers` | string \| object | LSP 설정 (코드 인텔리전스) | `"./.lsp.json"` |

---

## 허용된 필드 목록 (전체)

```typescript
interface PluginManifest {
  // 필수
  name: string;

  // 메타데이터 (선택)
  version?: string;
  description?: string;
  author?: {
    name?: string;
    email?: string;
    url?: string;
  };
  homepage?: string;
  repository?: string;
  license?: string;
  keywords?: string[];

  // 컴포넌트 경로 (선택)
  commands?: string | string[];
  agents?: string | string[];
  skills?: string | string[];
  hooks?: string | object;
  mcpServers?: string | object;
  outputStyles?: string | string[];
  lspServers?: string | object;
}
```

---

## 허용되지 않는 필드

다음 필드들은 **사용할 수 없습니다**:

```json
// ❌ 잘못된 필드들 - 절대 사용 금지
{
  "category": "...",        // ❌ 지원 안함
  "dependencies": [...],    // ❌ 지원 안함
  "main": "...",           // ❌ 지원 안함
  "scripts": {...},        // ❌ 지원 안함
  "config": {...},         // ❌ 지원 안함
  "private": true,         // ❌ 지원 안함
  "engines": {...},        // ❌ 지원 안함
  "peerDependencies": {...}, // ❌ 지원 안함
  "devDependencies": {...},  // ❌ 지원 안함
  "type": "...",           // ❌ 지원 안함
  "exports": {...},        // ❌ 지원 안함
  "files": [...],          // ❌ 지원 안함
  "bin": {...}             // ❌ 지원 안함
}
```

**참고**: `category`는 `marketplace.json`에서만 사용됩니다. `plugin.json`에서는 사용 불가.

---

## 올바른 예시

### 최소 구성

```json
{
  "name": "my-plugin"
}
```

### 기본 구성

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "플러그인 설명",
  "author": {
    "name": "ddingg"
  },
  "keywords": ["keyword1", "keyword2"]
}
```

### 전체 구성

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "플러그인 설명",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

---

## 경로 규칙

1. **모든 경로는 플러그인 루트 기준 상대 경로**
2. **반드시 `./`로 시작**
3. **커스텀 경로는 기본 디렉토리를 대체하지 않고 추가됨**

```json
// ✅ 올바른 경로
{
  "commands": "./custom/commands/",
  "agents": ["./custom-agents/reviewer.md", "./custom-agents/tester.md"]
}

// ❌ 잘못된 경로
{
  "commands": "custom/commands/",      // ./ 누락
  "agents": "/absolute/path/agents/"   // 절대 경로 사용
}
```

---

## 환경 변수

`${CLAUDE_PLUGIN_ROOT}`: 플러그인 디렉토리의 절대 경로

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 검증 체크리스트

plugin.json 작성 시 확인:

- [ ] `name` 필드가 존재하는가?
- [ ] `name`이 kebab-case인가?
- [ ] 허용되지 않는 필드가 없는가?
- [ ] 모든 경로가 `./`로 시작하는가?
- [ ] JSON 문법이 올바른가?

---

## Anti-Patterns

### ❌ npm package.json 필드 사용

```json
// ❌ 잘못됨 - npm 전용 필드
{
  "name": "my-plugin",
  "main": "index.js",
  "scripts": {
    "build": "tsc"
  },
  "dependencies": {
    "lodash": "^4.0.0"
  }
}
```

### ✅ 올바른 plugin.json

```json
// ✅ 올바름 - Claude Code 플러그인 스키마만 사용
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "플러그인 설명",
  "author": {
    "name": "ddingg"
  }
}
```

### ❌ category 필드 사용

```json
// ❌ 잘못됨 - category는 marketplace.json에서만 사용
{
  "name": "my-plugin",
  "category": "development"
}
```

### ✅ marketplace.json에서 category 사용

```json
// marketplace.json
{
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin",
      "category": "development"  // ✅ 여기서만 사용
    }
  ]
}
```
