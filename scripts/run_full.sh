#!/usr/bin/env bash
# Full-scope experiment for the GenLoc-Java pipeline.
#
# Usage:
#   full <project> <repo_path> <bug_report_xml> [embedding]
#
# Example (tomcat is bundled in the image):
#   full tomcat /artifact/repos/tomcat \
#        /artifact/dataset/ye-et-al-dataset/tomcat.xml openai
#
# For other Ye et al. projects, mount or clone the corresponding repository and
# point <repo_path> at it. By default ALL bugs (latest 40%, as in the paper) are
# processed; export GENLOC_MAX_BUGS to cap the count.
set -euo pipefail

PROJECT="${1:?usage: full <project> <repo_path> <xml> [embedding]}"
REPO="${2:?usage: full <project> <repo_path> <xml> [embedding]}"
XML="${3:?usage: full <project> <repo_path> <xml> [embedding]}"
EMBEDDING="${4:-openai}"

cd /artifact/source-code/GenLoc-Java

echo "==> [1/4] Embedding-based retrieval (project=$PROJECT, embedding=$EMBEDDING)"
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

echo "==> Full experiment for '$PROJECT' complete. Results in /artifact/output/"
