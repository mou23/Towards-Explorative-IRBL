#!/usr/bin/env bash
# Full-scope experiment for the GenLoc-Python pipeline on SWE-bench Lite.
#
# WARNING: this is the FULL scope. It downloads the SWE-bench Lite dataset from
# the Hugging Face Hub and clones 12 large repositories (several GB, network
# required) into ../swe_lite_repos. It is NOT the reduced/offline scope — use
# the Java image's `smoke`/`reduced` modes for the one-day validation.
set -euo pipefail

SRC=/artifact/source-code/GenLoc-Python
REPOS_DIR=/artifact/swe_lite_repos
URLS=/artifact/dataset/swe-bench-lite/project-repository-urls.txt

mkdir -p "$REPOS_DIR"

echo "==> Cloning SWE-bench Lite repositories (this may take a long time)"
while IFS= read -r url; do
  [[ -z "$url" ]] && continue
  name="$(basename "$url")"
  if [[ ! -d "$REPOS_DIR/$name/.git" ]]; then
    echo "    cloning $name ..."
    git clone "$url" "$REPOS_DIR/$name"
  else
    echo "    $name already present, skipping"
  fi
done < "$URLS"

# GenLoc-Python expects repositories at ../swe_lite_repos relative to the source
# directory.
ln -sfn "$REPOS_DIR" "$(dirname "$SRC")/swe_lite_repos"

cd "$SRC"

echo "==> [1/4] Embedding-based retrieval (loads SWE-bench Lite from Hugging Face)"
python main.py

echo "==> [2/4] LLM-based ranking"
python bug_localizer.py

echo "==> [3/4] Post-processing"
python post_processor.py .

echo "==> [4/4] Evaluation metrics"
python evaluation_metric_calculator.py

mkdir -p /artifact/output
cp -f ./*_final_ranked_output.csv /artifact/output/ 2>/dev/null || true
cp -f ./*_intermediate_ranking.csv /artifact/output/ 2>/dev/null || true

echo "==> Python full experiment complete. Results in /artifact/output/"
