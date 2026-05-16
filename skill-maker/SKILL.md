---
name: skill-maker
description: Create new skills and maintain existing SKILL.md files. Use when the user wants to create a skill directory and SKILL.md from scratch, add Python scripts to a skill, update skill instructions or frontmatter, or review a SKILL.md.
---

# Skill Maker

Create and maintain Agent Skills — directories containing a `SKILL.md` and optional supporting files.

## Directory structure

```txt
skill-name/
├── SKILL.md
├── scripts/  # Optional
└── ...
```

## SKILL.md

For guidelines on writing `SKILL.md` files for [Agent Skills](https://agentskills.io/home), refer to:

- [skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- [Best practices](https://agentskills.io/skill-creation/best-practices.md)
- [Spec](https://agentskills.io/specification.md)


### Body

Follow [llm-friendly-md](../llm-friendly-md/SKILL.md).

## Scripts

- For simple automation prefer `.sh` or `.bat`.
- Use Python when the task is too complex for shell scripts. Refer to [scripts/python.md](scripts/python.md).

## Workflow

1. Create `skill-name/` and `skill-name/SKILL.md`.
2. Write frontmatter: `name` matching the directory, `description` covering what and when.
3. Write the body: rules, workflow, examples.
4. Add scripts if needed, following the Python script guidelines if using Python.
5. Validate markdown: `python3 ../llm-friendly-md/scripts/check.py SKILL.md`.
