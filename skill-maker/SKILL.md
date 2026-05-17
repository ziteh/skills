---
name: skill-maker
description: Create new skills, modify and improve existing skills. Use when users want to write a new skill from scratch, refine an existing SKILL.md, optimize a skill's description for better triggering accuracy, add supporting scripts.
---

# Skill Maker

Create and maintain Agent Skills — directories containing a `SKILL.md` and optional supporting files.

## Creating a skill

### Capture intent

Start by understanding what the user actually wants. If the user says something like "turn this into a skill," extract the requirement from the current conversation. If the user says "I need a skill to do X," make sure the goal is clear and that you understand what success looks like. When the intent is ambiguous, ask clarifying questions until both sides agree on the requirement.

Key questions to confirm:

- What is the primary purpose of this skill?
- When should it trigger?
- What are the expected inputs and outputs?

### Research

Actively probe for edge cases, constraints, positive/negative examples, and whether scripts or reference files are needed. Read relevant docs, specs, and best practices to build a complete picture of the requirements.

If the request seems like an anti-pattern, unconventional, or a poor fit for a skill, surface that concern and explain the tradeoff or a better alternative — but let the user make the final call.

### Write the SKILL.md

Create a new directory named after the skill and place a `SKILL.md` inside it.

```txt
skill-name/
└── SKILL.md
```

Begin `SKILL.md` with frontmatter containing `name` and `description`.

```md
---
name: skill-name
description: Clearly describe what this skill does and when it triggers.
---

# Skill Name
```

The `description` field is critical — it controls when the skill is selected. Write it to be clear, specific, and action-oriented, with concrete trigger examples. Avoid vague or generic phrasing. Refer to the [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md).

```yaml
# Bad - too vague, not actionable
description: Helps with PDFs.

# Good - clear, actionable, with trigger examples
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
```

Write the body clearly and concisely: purpose, usage, supported inputs, positive/negative examples. Keep the structure logical.

If the content grows long or spans multiple domains, split it into separate files and link to them from `SKILL.md`.

Some skills are spec-like with strict rules — use RFC 2119 keywords (MUST, SHOULD, MAY) there. Others are general-purpose and benefit from a flexible tone: explain the reasoning behind each guideline rather than mandating it, so the skill remains adaptable rather than brittle.

Refer to the [Best Practices](https://agentskills.io/skill-creation/best-practices.md).

### Scripts

If the skill requires automation, add scripts in a `scripts/` (or other appropriate folder name) subdirectory.

- Prefer `.sh` or `.bat` for simple automation.
- Use Python for complex logic. See [scripts/python.md](scripts/python.md).

Regardless of the method used, there are some general rules:

- **Avoid interactive:** Scripts SHOULD NOT require user interaction during execution. This ensures they can run unattended and be integrated into automated workflows.
- **Usage help:** Scripts SHOULD provide usage information when invoked with `--help`. The agent will naturally use `--help` to learn how to use this script.
- **Structured output:** Scripts SHOULD use structured formats (JSON, CSV, etc.) over free-form text. This helps the agent better understand and allows for combination with pipelines.
- **Helpful error messages:** Scripts SHOULD provide helpful error messages so that the agent knows how to correct the issue. For example, it should output `Error: The specified file 'path/to/file.md' is not supported; accepts only .txt, .csv, .tsv` rather than `Error: Invalid data.`
- **Separate data from diagnostics:** Progress, logs, debug, and the like SHOULD be written to stderr; stdout SHOULD be used only for outputting clean and parsable data.
- **Meaningful exit codes:** Scripts SHOULD use exit codes to indicate success (0) or failure (non-zero). This allows the agent to detect errors programmatically. If the script does not need to produce any output when it succeeds, it should exit silently with an exit code of 0.
- **Idempotency:** Scripts SHOULD ensure that running them multiple times produces the same result without unintended side effects. This allows the agent to safely retry.
- **Dry-run mode:** For destructive or stateful operations, a `--dry-run` flag SHOULD be provided to allow previewing what will happen.
