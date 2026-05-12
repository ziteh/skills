---
name: mvp-script
description: Write simple, quick scripts (.sh, .bat) for MVPs or prototypes.
---

# MVP Script

Scripts in MVP/prototype contexts should be **ugly, fast, and obviously correct**. The goal is to validate quickly, not to impress. These concepts apply to any script (even if only using .sh as an example).

## The Core Rules

**No decorative output**
Never add visual banners, dividers, or section headers. Only print what you actually need to see.

```bash
# DON'T
echo "=================="
echo "Create folder"
echo "=================="
mkdir output

# DO
echo "Create folder"
mkdir output
```

**No numbering**
Step numbers go stale the moment you insert or reorder a step. Omit them entirely.

```bash
# DON'T
echo "Step 1: Build"
npm run build

# DO
echo "Building assets"
npm run build
```

**Only log what you can't see otherwise**
Log runtime-dependent values (paths, URLs, IDs) — they're invisible from the code itself. Don't log actions that are self-evident.

```bash
# DON'T — the action is obvious; the variable value is not
echo "Copying files"
cp -r src/ "$DEST_DIR"

# DO
echo "Dest dir: $DEST_DIR"
cp -r src/ "$DEST_DIR"
```

**Fail fast**
No retries, no fallback, no friendly error messages. Let it crash with the raw error.

```bash
# DON'T
if ! mkdir -p "$DIR"; then
  echo "Error: Could not create directory $DIR. Please check permissions."
  exit 1
fi

# DO
set -e
mkdir -p "$DIR"
```

Use `set -e` (and optionally `set -x` for debugging) at the top.

**Comment only non-obvious**
Comments should explain why — intent and constraint — not what. Never duplicate the `echo`.

```bash
# DON'T
echo "Get data"
# Get data from API via curl
curl https://example.com/api/data

# DO
echo "Get data from API"
curl https://example.com/api/data
```

```bash
# DON'T
sleep 10 # Wait for 10 seconds

# DO
sleep 10 # Avoid rate limiting
```

**Hardcode values**
No flags, no config files, no argument parsing. Hardcode values directly. For values that callers need to override, use an env var with a default instead.

```bash
# DON'T — argument parsing adds unnecessary complexity
OUTPUT_DIR="${1:-./output}"

# DO — hardcoded (nothing needs to vary)
BASE_URL="https://api.example.com"

# DO — env var with fallback (callers may need a different path)
OUTPUT_DIR="${OUTPUT_DIR:-./output}"
```

**Automation**
Scripts should be callable by AI agents or other programs without modification. No interactive prompts. Use exit codes to signal success/failure — don't make callers parse output.

```bash
# DON'T — blocks automation
read -p "Continue? (y/n) " confirm
[[ "$confirm" != "y" ]] && exit 1

# DON'T — caller can't detect failure reliably
if ! ./deploy.sh; then
  echo "Deploy failed"
fi

# DO — set -e propagates failures automatically; caller checks exit code
set -e
./deploy.sh
```
