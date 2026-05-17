---
name: llm-friendly-md
description: Write, improve, or evaluate Markdown intended for LLM consumption — including SKILL.md, AGENTS.md, prompt templates, agent specs, and any .md files an LLM will read or act upon.
---

# LLM-Friendly Markdown

Write for LLMs first, not general human-facing. Help LLMs better understand and adhere to the content, reduce token usage, and minimize semantic noise

> Keywords follow RFC 2119.

## Rules

### Document Structure

- A document MUST have exactly one H1. LLM retrievers treat H1 as the document title. Multiple H1s fragment the document's semantic identity.
- Heading levels MUST NOT be skipped (e.g., H2 directly to H4). Heading hierarchy infers parent-child containment; skipping levels breaks the implied tree, causing retrieved chunks to lose their governing context.
- Heading and list nesting SHOULD NOT exceed 3 levels. LLMs have limited ability to understand deeply nested structures.

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

- Content MUST be written in concise, precise English. Imprecise wording forces the LLM to make additional guesses.
- The conclusion, constraint, or action target SHOULD appear at the start of each paragraph. Placing the key term first reduces the need for long-range dependencies when the LLM resolves the meaning of subsequent clauses.
- Pleasantries and openers (e.g., "In this section, we will...") MUST NOT be used. Phrases like "In this section, we will..." carry zero semantic payload and shift the governing noun away from the actual subject.
- Double negatives SHOULD NOT be used. The double negative conceals the true intention.
- Pronouns SHOULD be replaced with concrete nouns to eliminate ambiguous reference. Pronouns like "it", "they", and "this" depend on co-reference context absent in isolated chunks.
- Specifications or requirements statements SHOULD include rationale so the LLM infers intent rather than following rules rigidly. However, for certain rules that require strict adherence, RFC 2119 keywords MAY be used; these keywords carry precise, standardized semantics.

**Bad:**

```md
In this section, we will discuss error handling. It is not uncommon to forget that errors should be logged.
```

**Good:**

```md
Errors MUST be written to `error.log`. Each log entry MUST include a timestamp and error code.
```

### Content Discipline

- Each concept SHOULD have a single source of truth; reference the concept elsewhere rather than repeating. Repeated definitions create divergent embeddings; retrieval may surface conflicting versions, introducing inconsistency.
- Common knowledge SHOULD be omitted; state only domain-specific logic and constraints. Repeating facts already known to the LLM (such as "SOP is a standard operating procedure") not only wastes tokens but also dilutes the key meaning.
- A document SHOULD use one term per concept; inconsistent naming increases embedding dispersion and ambiguity. Synonyms scatter a concept's representation across multiple points in the embedding space.

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

- Emoji, decorative dividers, and ASCII art MUST NOT be used. Emoji tokenize unpredictably; decorative elements increase token count without contributing to meaning.
- Bold, italics, and strikethrough SHOULD be used sparingly. Overuse can create noise.
- Bold MAY be used as a structural element, such as the key term in a definition-style list item. When bold consistently marks key terms, bold signals a structural pattern the LLM can recognize and use for extraction (term → definition).
- `inline code` SHOULD be used for all variable names, file paths, command names, and literal values. Backtick-enclosed strings are treated as literal identifiers by convention. Backtick wrapping also distinguishes semantically distinct forms such as `null` (the literal) and null (the concept).
- Unordered lists SHOULD be used by default; ordered lists MUST only be used when sequence is required. Ordered lists imply sequential dependency; applying them to non-sequential items introduces false ordering relationships.
- Heading titles MUST NOT include sequential numbers unless the sections have an explicit ordering relationship. Numbering headings implies priority or sequence where none exists.
- Lists SHOULD be preferred over tables. Lists can convey the same information with lower parsing overhead.
- Complex data structures SHOULD be represented using JSON. JSON's well-defined, machine-parseable structure enables reliable extraction by LLMs.
- Every code block SHOULD have a language tag, and SHOULD use the full name (e.g., `typescript` instead of `ts`). For code blocks that do not require syntax understanding (such as those describing directory structures), use `text`. Language tags enable syntax-aware parsing and prevent misidentification.
- Blockquotes MAY be used for quotations, callouts, or asides that are distinct from the main content. Blockquotes create a semantic boundary signaling that the content is subordinate or parenthetical to the main flow.
- CommonMark syntax SHOULD be used; GFM extensions and non-standard Markdown features SHOULD be avoided. Many extension syntaxes are designed to meet human rendering needs; non-standard syntax does not guarantee semantic consistency.

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

`scripts/count_tokens.py` estimates token usage, output in JSON format. Actual counts vary by model, but relative comparisons are valid.

- Default encoding (`cl100k_base`): `python3 scripts/count_tokens.py SKILL.md`
- Other encoding: `python3 scripts/count_tokens.py SKILL.md --encoding o200k_base`

`scripts/spell_check.py` checks spelling in prose, ignoring fenced code blocks and inline code. Uses spaCy for tokenisation and pyspellchecker for dictionary lookup. Output is JSONL — one object per suspected misspelling. The spell-check results are for reference only; it may misidentify some proper nouns.

- Check a file: `python3 scripts/spell_check.py SKILL.md`
- Other language: `python3 scripts/spell_check.py SKILL.md --lang es`

Each output line has the form `{"line": <n>, "word": "<word>", "suggestions": [...]}`.
