#!/usr/bin/env bash
# Reduced-scope experiment (validatable in well under one day):
# runs the full GenLoc-Java pipeline on the most recent bugs of the tomcat
# project. Defaults to 10 bugs (the minimum demonstration set); override with
# GENLOC_MAX_BUGS.
set -euo pipefail

PROJECT=tomcat
REPO=/artifact/repos/tomcat
XML=/artifact/dataset/ye-et-al-dataset/tomcat.xml
EMBEDDING=openai

export GENLOC_MAX_BUGS="${GENLOC_MAX_BUGS:-10}"

cd /artifact/source-code/GenLoc-Java

echo "==> [1/4] Embedding-based retrieval (GENLOC_MAX_BUGS=$GENLOC_MAX_BUGS)"
python main.py "$PROJECT" "$REPO" "$XML" "$EMBEDDING"

echo "==> [2/4] LLM-based ranking"
python bug_localizer.py "$PROJECT" "$XML"

echo "==> [3/4] Post-processing"
python post_processor.py "$PROJECT"

echo "==> [4/4] Evaluation metrics"
python evaluation_metric_calculator.py "$PROJECT"

mkdir -p /artifact/output
cp -f "${PROJECT}_intermediate_ranking.csv" /artifact/output/ 2>/dev/null || true
cp -f "${PROJECT}_final_ranked_output.csv"  /artifact/output/ 2>/dev/null || true

echo "==> Reduced experiment complete. Results copied to /artifact/output/"
