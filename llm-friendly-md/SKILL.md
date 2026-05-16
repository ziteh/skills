---
name: llm-friendly-md
description: Guides writing LLM-friendly Markdown optimized for token efficiency, semantic clarity, and retrieval precision. Use whenever writing or reviewing any Markdown document intended for AI consumption — including SKILL.md, CLAUDE.md, AGENTS.md, prompt templates, system prompts, README files for AI tools, or any .md file that an LLM will read, parse, or act on.
---

# LLM-Friendly Markdown

Write for LLMs first, not general human-facing. Optimize for token efficiency, semantic clarity, and retrieval precision — not visual polish.

> Keywords follow RFC 2119.

## Rules

### Document Structure

- A document MUST have exactly one H1.
- Heading levels MUST NOT be skipped (e.g., H2 directly to H4).
- Heading and list nesting SHOULD NOT exceed 3 levels.

**Bad:**

```md
# My Guide

# Usage (multiple H1)

### Steps (skipped H2)
```

**Good:**

```md
# My Guide

## Usage

### Steps
```

### Language and Clarity

- Content MUST be written in concise, precise English.
- Front-loading: The conclusion, constraint, or action target MUST appear at the start of each paragraph.
- Pleasantries and openers (e.g., "In this section, we will...") MUST NOT be used.
- Double negatives MUST NOT be used.
- Pronouns SHOULD be replaced with concrete nouns to eliminate ambiguous reference.
- When expressing the degree of constraint, the RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) MAY be used.

**Bad:**

```md
In this section, we will discuss error handling. It is not uncommon to forget that errors should be logged.
```

**Good:**

```md
Errors MUST be written to `error.log`. Each log entry MUST include a timestamp and error code.
```

### Content Discipline

- Single Source of Truth: Each concept SHOULD be defined in exactly one place; reference it elsewhere rather than repeating.
- Common knowledge SHOULD be omitted; state only domain-specific logic and constraints.
- A document MUST use one term per concept; inconsistent naming increases embedding dispersion and ambiguity.

**Bad:**

```md
## Auth

A token is a signed JWT issued on login.

## Session

An access token (i.e. the JWT credential) expires after 1 hour.
```

**Good:**

```md
## Auth

A **token** is a signed JWT issued on login. Tokens expire after 1 hour.

## Refresh

Expired tokens (see Auth) MAY be exchanged for a new token via `POST /refresh`.
```

### Formatting

- Emoji, decorative dividers, and ASCII art MUST NOT be used.
- Bold, italic, and strikethrough SHOULD NOT be used for visual emphasis.
- Bold MAY be used as a structural element, such as the key term in a definition-style list item.
- `inline code` MUST be used for all variable names, file paths, command names, and literal values.
- Unordered lists SHOULD be used by default; ordered lists MUST only be used when sequence is required.
- Heading titles MUST NOT include sequential numbers unless the sections have an explicit ordering relationship.
- Lists SHOULD be preferred over tables.
- Every code block MUST have a language tag.
- Blockquotes MAY be used for quotations, callouts, or asides that are distinct from the main content.
- CommonMark syntax MUST be used; GFM extensions and non-standard Markdown features SHOULD be avoided.

**Bad:**

````md
📁 These are some common _data interchange formats_!

| Format | Full Name                  |
| ------ | -------------------------- |
| JSON   | JavaScript Object Notation |
| YAML   | YAML Ain't Markup Language |

```
git pull
```

> [!NOTE]
> This is a GitHub-specific Alerts block.
````

**Good:**

````md
Common data interchange formats:

- **JSON**: JavaScript Object Notation
- **YAML**: YAML Ain't Markup Language

```sh
git pull
```

> **Note:** Basic syntax is sufficient.
````

## Skills

For guidelines on writing `SKILL.md` files for [Agent Skills](https://agentskills.io/home), refer to:

- [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- [Best practices](https://agentskills.io/skill-creation/best-practices.md)
- [Spec](https://agentskills.io/specification.md)

## Drafting Process

1. **Outline Core Concepts**: identify the specific constraints, logic, or formats the LLM lacks.
2. **Define Terminology**: pick exactly one term for each concept and use it throughout.
3. **Draft Sections**: apply the structure and language rules in this guide.
4. **Refine and Strip**: remove all pleasantries, visual formatting, over-explanations, and pronouns.

## Validation

`scripts/check.py` validates `.md` files. The venv is created automatically on first run.

- Single file: `python3 scripts/check.py SKILL.md`
- Directory (recursive): `python3 scripts/check.py docs/`
- Mixed: `python3 scripts/check.py SKILL.md docs/`
