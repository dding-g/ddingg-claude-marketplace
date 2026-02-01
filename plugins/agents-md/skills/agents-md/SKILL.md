---
name: agents-md
description: AGENTS.md authoring patterns. Activated when writing AI agent context files, working with agents.md or AGENTS.md.
---

# AGENTS.md Authoring Patterns

> Vercel research: Skills 53% → AGENTS.md 100% pass rate. Passive context beats on-demand skill invocation.

## Why AGENTS.md Over Skills

|Approach|Reliability|Reason|
|---|---|---|
|Skills|~53% invocation|Trigger instability, wording-sensitive|
|Explicit skill hints|~95%|Still fragile to prompt changes|
|AGENTS.md|100%|Always loaded in context|

## File Structure

### Basic Structure

```markdown
# Project Name

## Tech Stack
React 19, Next.js 15 (App Router), TypeScript 5.7, Tailwind CSS 4

## Architecture
- FSD (Feature-Sliced Design)
- Server Components default, 'use client' minimal

## Conventions
- Components: PascalCase, files: kebab-case
- barrel export: entities/features index.ts only

## Patterns
|state: react-query (server), zustand (client)
|forms: @tanstack/form + zod standard schema

## Commands
|dev: bun dev
|build: bun run build
|test: bun run test

## DO NOT
- any type
- console.log in commits
- useEffect for data fetching (use react-query)
```

### Compressed Index Structure (Large docs)

40KB → 8KB (80% compression) with same performance. Provide an **index map** for agent retrieval.

```markdown
[Docs Index]|root: ./.project-docs
|IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning
|api/:{auth.md,users.md,payments.md}
|patterns/:{state-management.md,data-fetching.md,error-handling.md}
|guides/:{setup.md,deployment.md,testing.md}
```

### Hierarchical Placement

```
project-root/
├── AGENTS.md              # Global conventions, tech stack
├── apps/
│   ├── web/
│   │   └── AGENTS.md      # Web-specific rules
│   └── mobile/
│       └── AGENTS.md      # Mobile-specific rules
├── packages/
│   └── ui/
│       └── AGENTS.md      # UI library rules
└── .project-docs/         # Reference docs directory
```

- Root AGENTS.md: project-wide common rules
- Sub AGENTS.md: directory-scoped rules (inherits parent rules)

## Writing Strategy

### Retrieval-led Reasoning

```markdown
## IMPORTANT
- Check .project-docs/ before using framework APIs
- Prioritize project docs over pre-trained knowledge
- Read docs first when uncertain, then write code
```

### Token-Saving Compression

```markdown
# BEFORE (verbose) - 200 tokens
## State Management
We use React Query for server state management. All queries should use
the queryOptions pattern defined in the entities layer.

# AFTER (compressed) - 50 tokens
## State
|server: react-query (queryOptions pattern, entities layer)
|client: zustand stores
```

### Conditional Detail Docs

```markdown
## API Patterns
|IMPORTANT: Read .project-docs/api-patterns.md when writing APIs
|summary: queryOptions + mutationOptions, Key Factory required
|details: ./.project-docs/api-patterns.md
```

### Negative Instructions (DO NOT)

```markdown
## DO NOT
- any type
- console.log in commits
- re-export internals from index.ts (public API only)
- useEffect for data fetching (use react-query)
```

Negative instructions effectively prevent common agent mistakes.

## Auto-Generation

For Next.js projects:

```bash
npx @next/codemod@canary agents-md
```

This detects framework version, downloads matching docs, and injects compressed index into AGENTS.md.

## DO NOT

- Inline entire documentation in AGENTS.md (use index references)
- Write vague instructions ("write good code")
- Rely solely on Skills for critical patterns (56% failure rate)
- Omit DO NOT section (agents need explicit negative guidance)
