# Optimize Skills Command

> Analyze all SKILL.md files and report optimization opportunities

## Usage

```
/optimize-skills
```

## Analysis Steps

### 1. Find all SKILL.md files

```bash
find plugins -name "SKILL.md" -type f
```

### 2. For each SKILL.md, check and report

**Line count** (warn if > 500 lines):
```bash
wc -l <file>
```

**Korean text detection** (should be English):
Check for Korean characters (Hangul range U+AC00-U+D7AF, U+1100-U+11FF) in prose sections.

**Missing DO NOT section**:
Check for `## DO NOT` heading.

**Redundant sections**:
Check for `## Overview` or `## Activation` headings — these are redundant with frontmatter `description`.

**Frontmatter validation**:
- Must have `---` delimited frontmatter
- Must contain `name:` field
- Must contain `description:` field
- `description` should be in English

### 3. Duplicate content detection

Compare code blocks and section headings across all SKILL.md files to identify overlapping content that could be consolidated.

### 4. Token estimation

Estimate tokens per file (roughly 1 token per 4 characters).

## Output Format

```markdown
## SKILL.md Optimization Report

### Summary
- Total skills: N
- Total lines: N
- Estimated tokens: ~N

### Per-File Analysis

| File | Lines | Est. Tokens | Issues |
|------|-------|-------------|--------|
| plugins/common-skills/.../fsd-architecture/SKILL.md | 188 | ~2.1k | - |
| plugins/nextjs-app-router/.../SKILL.md | 380 | ~4.2k | WARN: >300 lines |

### Issues Found

#### Korean Text Detected
- `plugins/.../SKILL.md` line 45: "컴포넌트 구조"

#### Missing DO NOT Section
- `plugins/.../SKILL.md`

#### Redundant Sections (Overview/Activation)
- `plugins/.../SKILL.md`: has ## Overview (redundant with frontmatter)

#### Large Files (>500 lines)
- `plugins/.../SKILL.md`: 556 lines

### Recommendations
- [Specific suggestions for each issue]
```

## Auto-Fix Options

After reporting, offer to:
1. Remove detected `## Overview` / `## Activation` sections
2. Add missing `## DO NOT` sections with placeholder
3. Translate detected Korean text to English
