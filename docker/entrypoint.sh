#!/usr/bin/env bash
# Entrypoint for the GenLoc artifact images. Sets up the OpenAI API key from the
# environment (or a mounted file) and dispatches to the requested run mode.
set -euo pipefail

# --- OpenAI API key setup ---------------------------------------------------
# Reviewers provide their key either via the OPENAI_API_KEY environment variable
#   docker run -e OPENAI_API_KEY=sk-... ...
# or by mounting a file to /artifact/source-code/api_key.txt. GenLoc reads the
# key from a plain-text file (../api_key.txt for the Java pipeline, api_key.txt
# for the Python pipeline), so we materialise it at every expected location.
KEY_PATHS=(
  /artifact/source-code/api_key.txt
  /artifact/source-code/GenLoc-Java/api_key.txt
  /artifact/source-code/GenLoc-Python/api_key.txt
)
if [[ -n "${OPENAI_API_KEY:-}" ]]; then
  for p in "${KEY_PATHS[@]}"; do
    mkdir -p "$(dirname "$p")"
    printf '%s' "$OPENAI_API_KEY" > "$p"
  done
fi

if [[ ! -s /artifact/source-code/api_key.txt && ! -s /artifact/source-code/GenLoc-Python/api_key.txt ]]; then
  echo "WARNING: No OpenAI API key found." >&2
  echo "         Provide one with: docker run -e OPENAI_API_KEY=sk-... ..." >&2
  echo "         or mount a file to /artifact/source-code/api_key.txt" >&2
fi

# --- Dispatch ---------------------------------------------------------------
cmd="${1:-smoke}"
case "$cmd" in
  smoke)       exec /artifact/scripts/run_smoke_test.sh ;;
  reduced)     exec /artifact/scripts/run_reduced.sh ;;
  full)        shift; exec /artifact/scripts/run_full.sh "$@" ;;
  python-full) exec /artifact/scripts/run_python_full.sh ;;
  *)           exec "$@" ;;
esac
