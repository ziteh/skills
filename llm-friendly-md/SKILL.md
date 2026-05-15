---
name: llm-friendly-md
description: Guide writing Markdown that is easy for LLMs and AI to parse, follow, and act on. Use when writing any .md document for LLMs or AI that includes, but not limited to, SKILL.md, and AGENTS.md.
---

# LLM Friendly Markdown

Write for LLMs first, not general human-facing. Optimize for token efficiency, semantic clarity, and retrieval precision — not visual polish.

> Keywords follow RFC 2119.

## The Core Rules

### Document Structure

- A document MUST have exactly one H1.
- Heading levels MUST NOT be skipped (e.g., H2 directly to H4).
- Heading and list nesting SHOULD NOT exceed 3 levels.

### Language and Clarity

- Content MUST be written in concise, precise English.
- Front-loading: the conclusion, constraint, or action target MUST appear at the start of each paragraph.
- Pleasantries and openers (e.g., "In this section, we will...") MUST NOT be used.
- Double negatives MUST NOT be used.
- Pronouns SHOULD be replaced with concrete nouns to eliminate ambiguous reference.
- When expressing the degree of constraint, the RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) SHOULD be used.

### Content Discipline

- Single Source of Truth: each concept SHOULD be defined in exactly one place; reference it elsewhere rather than repeating.
- Common knowledge SHOULD be omitted; state only domain-specific logic and constraints.
- A document MUST use one term per concept; inconsistent naming increases embedding dispersion and ambiguity.

### Formatting

- Emoji, decorative dividers, and ASCII art MUST NOT be used.
- Bold, italic, and strikethrough SHOULD NOT be used unless the semantic distinction cannot be expressed with structure or word choice alone.
- `inline code` MUST be used for all variable names, file paths, command names, and literal values.
- Unordered lists SHOULD be used by default; ordered lists MUST only be used when sequence is required.
- Heading titles MUST NOT include sequential numbers unless the sections have an explicit ordering relationship.
- Lists SHOULD be preferred over tables.
- Every code block MUST have a language tag.
- Blockquotes SHOULD be used only for external references or notes that are distinct from the main content.

### Compatibility

- CommonMark syntax MUST be used; GFM extensions and non-standard Markdown features MUST NOT be used.

## Drafting Process

1. Outline Core Concepts: identify the specific constraints, logic, or formats the LLM lacks.
2. Define Terminology: pick exactly one term for each concept and use it throughout.
3. Draft sections applying the structure and language rules in this guide.
4. Refine and Strip: remove all pleasantries, visual formatting, over-explanations, and pronouns.

## Gotchas

- Do not use tables for large text blocks; LLMs parse linear lists better.
- Do not write intro text like "Here are the rules..."; start directly with constraints.
- Avoid pronouns across blocks; replace "It should be JSON" with "The payload MUST be JSON".

## Examples

Bad (Human-optimized, verbose, decorative):

```md
👋 **Welcome to the DB guidelines!**
In this section, we will cover how to query the database (DB). First, you should always check if `deleted_at` is null. Also, remember to only use our special helper for auth.
```

Good (LLM-optimized, direct, strict):

```md
- Queries MUST include `WHERE deleted_at IS NULL` (soft deletes are used).
- The `auth_helper.py` script MUST be used for all authentication.
```
