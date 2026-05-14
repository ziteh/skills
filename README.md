# Skills

My [Agent Skills](https://agentskills.io/home)

## Installation

Symlink each skill folder into Claude Code's skills directory:

```bash
ln -s /path/to/skills/<SKILL_FOLDER> ~/.claude/skills/<SKILL_FOLDER>
```

## Validation

Uses `skills-ref` to validate SKILL.md files.

```bash
./validate.sh
```

or 

```bash
cd agentskills/skills-ref
uv sync
source .venv/bin/activate

skills-ref validate ../../<SKILL_FOLDER>
```
