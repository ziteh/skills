---
name: mvp-script
description: Write simple, quick scripts (.sh, .bat) for MVPs or prototypes.
---

# MVP Script

Scripts in MVP/prototype contexts should be **ugly, fast, and obviously correct** — validate quickly, not impress.

## The Core Rules

> Keywords follow RFC 2119.

### No numbering

- MUST NOT use step numbers. They go stale when steps are inserted or reordered.

```bash
# DON'T
echo "Step 1: Build"
npm run build

# DO
echo "Build"
npm run build
```

### Only log what you can't see otherwise

- MUST log runtime-dependent values (paths, URLs, IDs).
- MUST NOT log self-evident actions.

```bash
# DON'T — logs the action, not the value that matters
echo "Copying files"
cp -r src/ "$DEST_DIR"

# DO — logs the value; the action is self-evident
echo "Dest dir: $DEST_DIR"
cp -r src/ "$DEST_DIR"
```

### Fail fast

- MUST NOT add retries, fallbacks, or friendly error messages. Let it crash with the raw error.

```bash
# DON'T
if ! mkdir -p "$DIR"; then
  echo "Error: Could not create directory $DIR. Please check permissions."
  exit 1
fi

# DO
set -euo pipefail  # -u catches unbound vars; pipefail catches silent pipe failures
mkdir -p "$DIR"
```

Use `set -euo pipefail` (and optionally `set -x` for debugging) at the top.

### Only comment the non-obvious

Comments:

- MUST explain why — intent and constraint — not what.
- MUST NOT duplicate the `echo`.

```bash
# DON'T
sleep 10 # Wait for 10 seconds

# DO
sleep 10 # Avoid rate limiting
```

```bash
# DON'T
echo "Get data"
# Get data from API via curl
curl https://example.com/api/data

# DO
echo "Get data"
curl https://example.com/api/data
```

### Automation

Scripts:

- MUST be fully autonomous.
- MUST NOT use interactive prompts.
- MUST use exit codes to signal success/failure.

```bash
# DON'T — blocks automation
read -p "Continue? (y/n) " confirm
[[ "$confirm" != "y" ]] && exit 1

# DON'T — failure is swallowed; outer script still exits 0
if ! ./deploy.sh; then
  echo "Deploy failed"
fi

# DO — set -euo pipefail propagates failures automatically; caller checks exit code
set -euo pipefail
./deploy.sh
```

### No decorative output

- SHOULD NOT add visual banners, dividers, or section headers.
- Exception: MAY use decoration to highlight a final result.

```bash
# DON'T — decorates a routine step
echo "=================="
echo "Create folder"
echo "=================="
mkdir output

# DO — no decoration for routine steps
echo "Create folder"
mkdir output

# OK — decoration draws attention to the final result
echo "=================="
echo "Output: $RES_FILE"
echo "Failed: $FAILED_CNT/$TOTAL_CNT"
```

## Workflow

- Run scripts after writing; verify it behaves as expected.
- On unexpected behavior: add debug output (`set -x`, `echo`) → diagnose → fix → keep only the messages that matter at runtime and remove any temporary debug messages.
- On repeated failure: decompose → test parts independently → integrate.
