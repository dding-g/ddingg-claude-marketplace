---
name: onboarding-guide
description: Codebase onboarding guide. Activated when starting a new project analysis, requesting systematic codebase understanding, or running /onboard.
---

# Codebase Onboarding Guide

> Systematically understand a new codebase

## 5-Step Onboarding Process

### Step 1: High-Level Overview

|Action|Details|
|---|---|
|Identify the problem|What does this project solve?|
|Know the users|B2B, B2C, internal tool?|
|Core features|Top 3 features|
|Tech stack|Check package.json, README|

Key files: `README.md`, `package.json`, company Wiki/Confluence

### Step 2: Get It Running

```bash
1. Clone repository
2. Install dependencies (npm install, pip install, etc.)
3. Set up env vars (.env.example)
4. Start dev server
5. Test key features manually
```

Verify: local run, main features work, tests pass, build succeeds

### Step 3: Code Exploration

```
Exploration order:
1. Find entry points
2. Identify main routes/pages
3. Locate core business logic
4. Trace data flow
```

**Strategy: "Follow one feature end-to-end"**

Example: Login feature
1. Login button → onClick handler
2. Handler → API call
3. API → backend controller
4. Controller → service logic
5. Service → database
6. Response → frontend state update

### Step 4: Understand Patterns

|Pattern to Identify|What to Look For|
|---|---|
|Architecture|Layer structure, module boundaries|
|State management|Redux, Zustand, Context, React Query|
|API communication|REST, GraphQL, fetch patterns|
|Error handling|Boundaries, try/catch strategy|
|Testing|Unit, integration, E2E approach|
|Naming conventions|Files, components, variables|

Tips: Review recent PRs, find well-written files as benchmarks, use breakpoints for complex logic

### Step 5: Start Contributing

Recommended first tasks:
1. Good First Issue labeled issues
2. Documentation improvements
3. Add tests
4. Small bug fixes
5. Minor refactoring

Before contributing: understand branch strategy, PR templates, CI/CD pipeline, code review process

## Analysis Commands

|Command|Description|
|---|---|
|`/analyze`|Full codebase structure analysis|
|`/architecture`|Architecture and design pattern analysis|
|`/dependencies`|External dependency analysis|
|`/conventions`|Code convention analysis|
|`/onboard`|Run full onboarding workflow|

## Onboarding Notes Template

```markdown
# [Project Name] Onboarding Notes

## Overview
- Purpose:
- Users:
- Core features:

## Tech Stack
- Frontend:
- Backend:
- Database:
- Infrastructure:

## Architecture
[Diagram or description]

## Key Modules
| Module | Location | Role |
|--------|----------|------|

## Domain Terms
| Term | Meaning |
|------|---------|

## Dev Setup
[Local run instructions]

## Common Commands
- Dev:
- Test:
- Build:

## Notes
- [Team-specific rules]
- [Gotchas]
```

## DO NOT

- Try to understand all code at once (focus on core flows first)
- Struggle alone for too long (ask after 30 min of being stuck)
- Ignore documentation (README, comments, test code are important docs)
- Ignore existing patterns (follow team conventions first)
- Suggest refactoring too early (spend at least 2 weeks understanding first)
