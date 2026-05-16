---
name: mvp-script
description: Write simple, quick scripts (.sh, .bat) for MVPs or prototypes. Use this skill whenever the user asks for a bash script, shell script, batch file, .sh, .bat, or says things like "write me a script to...", "automate X", "quick script for Y", or "just something that does Z." Trigger for any scripting task where speed and correctness matter more than polish.
---

# MVP Script

Scripts in MVP/prototype contexts should be **ugly, fast, and obviously correct** — validate quickly, not impress.

> Keywords follow RFC 2119.

## Rules

### No numbering

- SHOULD NOT use step numbers. They go stale when steps are inserted or reordered.

```sh
# DON'T
echo "Step 1: Build"
npm run build

# DO
echo "Build"
npm run build
```

### Only log what you can't see otherwise

- SHOULD log runtime-dependent values (paths, URLs, IDs).
- MUST NOT log self-evident actions.

```sh
# DON'T — logs the action, not the value that matters
echo "Copying files"
cp -r src/ "$DEST_DIR"

# DO — logs the value; the action is self-evident
echo "Dest dir: $DEST_DIR"
cp -r src/ "$DEST_DIR"
```

### Fail fast

- SHOULD NOT add retries, fallbacks, or friendly error messages. Let it crash with the raw error.

```sh
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

```sh
# DON'T
sleep 10 # Wait for 10 seconds

# DO
sleep 10 # Avoid rate limiting
```

```sh
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
- SHOULD NOT use interactive prompts.
- MUST use exit codes to signal success/failure.

```sh
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
- Exception: MAY use decoration to highlight a important message.

```sh
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
echo "=================="
```

## Windows Batch (.bat)

The same principles apply — fail fast, no step numbers, only log runtime values.

```bat
@echo off
setlocal enabledelayedexpansion

REM DON'T — step numbers go stale
echo Step 1: Build
call npm run build

REM DO
echo Build
call npm run build
```

```bat
REM DON'T — logs the action, not the value
echo Copying files
xcopy /E /I src "%DEST_DIR%"

REM DO — logs the value; action is self-evident
echo Dest dir: %DEST_DIR%
xcopy /E /I src "%DEST_DIR%"
```

Fail fast in .bat — check `%ERRORLEVEL%` after critical commands or use `|| exit /b 1`:

```bat
call npm run build || exit /b 1
call npm run test  || exit /b 1
```

## Scope

These rules apply to MVP/prototype/automation scripts — where speed and correctness are the goal. If the user says the script will go to production or needs error recovery, don't apply the fail-fast and no-retry rules blindly; ask what level of robustness they need.

## Workflow

- Write the script, then run it to verify it behaves as expected.
- On unexpected behavior: add debug output (`set -x` / `echo %VAR%`) → diagnose → fix → remove temporary debug messages before finishing.
- On repeated failure: decompose → test parts independently → integrate.
