#!/usr/bin/env bash
# Smoke test: runs the full GenLoc-Java pipeline on a single (most recent) bug
# of the tomcat project. Intended to confirm the installation works end to end
# within the 30-minute "Getting Started" budget.
set -euo pipefail

PROJECT=tomcat
REPO=/artifact/repos/tomcat
XML=/artifact/dataset/ye-et-al-dataset/tomcat.xml
EMBEDDING=openai

# Limit to a single bug unless the reviewer overrides it.
export GENLOC_MAX_BUGS="${GENLOC_MAX_BUGS:-1}"

cd /artifact/source-code/GenLoc-Java

echo "==> [1/4] Embedding-based retrieval (GENLOC_MAX_BUGS=$GENLOC_MAX_BUGS)"
python main.py "$PROJECT" "$REPO" "$XML" "$EMBEDDING"

echo "==> [2/4] LLM-based ranking"
python bug_localizer.py "$PROJECT" "$XML"

echo "==> [3/4] Post-processing"
python post_processor.py "$PROJECT"

echo "==> [4/4] Evaluation metrics"
python evaluation_metric_calculator.py "$PROJECT"

# Collect machine-readable outputs into the mounted volume.
mkdir -p /artifact/output
cp -f "${PROJECT}_intermediate_ranking.csv" /artifact/output/ 2>/dev/null || true
cp -f "${PROJECT}_final_ranked_output.csv"  /artifact/output/ 2>/dev/null || true

echo "==> Smoke test complete. Results copied to /artifact/output/"
