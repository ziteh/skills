#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SKILLS_REF="$REPO_ROOT/agentskills/skills-ref"

# Ensure Python venv
if [[ ! -d "$SKILLS_REF/.venv" ]]; then
    uv sync --project "$SKILLS_REF" --quiet
fi
source "$SKILLS_REF/.venv/bin/activate"

count=0
failed=0
while IFS= read -r skill_md; do
    ((count++))
    skill_dir="$(dirname "$skill_md")"
    if ! skills-ref validate "$skill_dir"; then
        ((failed++))
    fi
# Find all SKILL.md files that are exactly 2 levels deep
done < <(find "$REPO_ROOT" -mindepth 2 -maxdepth 2 -name "SKILL.md" -not -path "*/agentskills/*")

echo
echo "==================="
echo "Validation complete"
echo "Failed: $failed/$count"

exit $failed
