# Towards Explorative IRBL: Combining Semantic Retrieval with LLM-driven Iterative Code Exploration
This paper proposes GenLoc, a novel IRBL technique that combines semantic retrieval with LLM-driven iterative code exploration to identify buggy files. It operates in two primary steps to localize relevant files. First, it retrieves a set of semantically similar files using an embedding-based similarity approach. Next, it employs an LLM augmented with a set of custom-designed code exploration functions, which enable the model to iteratively reason over the bug report and interact with the code base.

## 🗂️ Directory Structure

* `source-code/`: Contains the source code of GenLoc along with execution instructions.
* `output-files/`: Ranked list produced by GenLoc (for each trial).
* `intermediate-files/`: Intermediate artifacts produced by GenLoc (for each dataset and trial).
* `localized-bugs/`: Contains bugs correctly localized by GenLoc.
* `dataset/`: Contains XML files and GitHub URLs of the projects used for bug localization.
* `results/`: Contains the results of the experiments.
* `docs/`: Contains implementation details and time-cost analysis.
---

# Artifact Evaluation (ISSTA 2026)

This section is the artifact main README. It has two parts: a **Getting Started**
guide (install + smoke test, completable in under 30 minutes) and **Step-by-step
instructions** for reproducing the experiments. See also
[`REQUIREMENTS.md`](REQUIREMENTS.md), [`STATUS.md`](STATUS.md), and
[`LICENSE`](LICENSE).

The artifact is packaged as Docker images:

* **GenLoc-Java** ([`Dockerfile.java`](Dockerfile.java)) — runs the Java pipeline
  on the *Ye et al.* dataset. It bundles the `tomcat` repository at build time;
  at run time it calls the OpenAI API for embeddings and ranking. This image
  serves the smoke test and the reduced one-day experiment.
* **GenLoc-Python** ([`Dockerfile.python`](Dockerfile.python)) — runs the Python
  pipeline on *SWE-bench Lite*. It downloads the dataset and target repositories
  at run time and is provided for the full scope only.

## Prerequisites

* Docker Engine 20.10+ with the Compose v2 plugin (see [`REQUIREMENTS.md`](REQUIREMENTS.md)).
* An **OpenAI API key** with access to `gpt-4o-mini` and `text-embedding-3-small`. API key has been personally provided to the ISSTA committee (with a limit of $5). Approximate cost: ~US$0.02 per bug.

## Getting Started

### 1. Provide your OpenAI API key

The key is passed through the `OPENAI_API_KEY` environment variable and never
baked into the image.

```bash
# Linux / macOS
export OPENAI_API_KEY=sk-...
```

```powershell
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."
```

### 2. Smoke test (≈ a few minutes)

Build and run the full four-phase pipeline on a **single** bug to confirm the
installation. The image is built automatically on first use (installing
dependencies and cloning the `tomcat` repository); the container is kept after
the run so you can inspect it:

```bash
docker compose run genloc-java
```

(equivalently `docker compose run genloc-java smoke`).

**Expected output.** The four phases print progress, and the final phase prints
ranking-accuracy metrics for the processed bug, ending with lines of the form:

```
==> [4/4] Evaluation metrics
accuracy@1: <pct>% (<n> out of <total> bugs)
accuracy@5: <pct>% (<n> out of <total> bugs)
accuracy@10: <pct>% (<n> out of <total> bugs)
MRR@ 10 <value>
MAP@ 10 <value>
==> Smoke test complete. Results copied to /artifact/output/
```

A `tomcat_final_ranked_output.csv` file (columns: `bug_id`,
`bug_report_analysis`, `suspicious_files`, `fixed_files`) appears in
`./output/java/`. The `suspicious_files` column holds a JSON object of the form
`{"ranked_list": [{"file": ..., "justification": ...}, ...]}`. Seeing these
metrics and this file confirms the artifact works.

> **Note.** The message `Failed to send telemetry event
> ClientCreateCollectionEvent: capture() takes 1 positional argument but 3 were
> given` can be safely ignored — it comes from a third-party library's telemetry
> and does not affect GenLoc's results.

## Step-by-step reproduction

### Reduced scope (validatable in well under 30 mins)

Runs the full pipeline on the 10 most recent `tomcat` bugs (the minimum
demonstration set):

```bash
docker compose run genloc-java reduced
```

Override the number of bugs with `GENLOC_MAX_BUGS`:

```bash
GENLOC_MAX_BUGS=20 docker compose run genloc-java reduced
```

> **⚠️ Warning.** Each bug consumes OpenAI API tokens (~US$0.02 per bug). Setting
> `GENLOC_MAX_BUGS` too high will increase the total cost proportionally and may
> exceed your API budget (e.g. the $5 limit provided to the ISSTA committee).
> Choose the value with the per-bug cost in mind.

Results (`tomcat_intermediate_ranking.csv`, `tomcat_final_ranked_output.csv`)
are written to `./output/java/`, and accuracy@{1,5,10}, MRR@10 and MAP@10 are
printed to the console.

### Full scope — GenLoc-Java (Ye et al. dataset)

To reproduce a full per-project run (all bugs of the latest 40%, as in the
paper) for the bundled `tomcat` project:

```bash
docker compose run genloc-java full tomcat \
    /artifact/repos/tomcat \
    /artifact/dataset/ye-et-al-dataset/tomcat.xml openai
```

For the other Ye et al. projects (`aspectj`, `birt`, `eclipse`, `jdt`, `swt`),
clone the corresponding repository (URLs in
[`dataset/ye-et-al-dataset/project-repository-urls.txt`](dataset/ye-et-al-dataset/project-repository-urls.txt)),
mount it into the container, and point the `full` command at it, e.g.:

```bash
docker compose run \
    -v /path/to/aspectj:/artifact/repos/aspectj \
    genloc-java full aspectj \
    /artifact/repos/aspectj \
    /artifact/dataset/ye-et-al-dataset/aspectj.xml openai
```

### Full scope — GenLoc-Python (SWE-bench Lite)

> **Network-heavy.** Downloads SWE-bench Lite from the Hugging Face Hub and
> clones 12 repositories (several GB).

```bash
docker compose run genloc-python
```

### Mapping to the paper's claims

The numbers reported in the paper are the averages over **three trials**. The
exact per-trial outputs we obtained are included so reviewers can inspect them
without re-running everything:

| Paper artifact | Where it lives |
| --- | --- |
| Ranked lists produced by GenLoc (per dataset, per trial) | [`output-files/`](output-files/) |
| Intermediate artifacts produced by GenLoc (per dataset, per trial) | [`intermediate-files/`](intermediate-files/) |
| Bugs correctly localized (per trial) | [`localized-bugs/`](localized-bugs/) |
| GenLoc vs. issue-localization techniques | [`results/Comparison of GenLoc against Issue Localization Techniques.csv`](results/Comparison%20of%20GenLoc%20against%20Issue%20Localization%20Techniques.csv) |
| GenLoc vs. non-LLM techniques | [`results/Comparison of GenLoc against Non-LLM based techniques.csv`](results/Comparison%20of%20GenLoc%20against%20Non-LLM%20based%20techniques.csv) |
| GenLoc vs. prior LLM-based IRBL (GHRB) | [`results/Comparison of GenLoc against prior LLM based IRBL techniques on GHRB dataset.csv`](results/Comparison%20of%20GenLoc%20against%20prior%20LLM%20based%20IRBL%20techniques%20on%20GHRB%20dataset.csv) |
| GenLoc vs. prior LLM-based IRBL (Ye et al.) | [`results/Comparison of GenLoc against prior LLM based IRBL techniques on Ye et al dataset.csv`](results/Comparison%20of%20GenLoc%20against%20prior%20LLM%20based%20IRBL%20techniques%20on%20Ye%20et%20al%20dataset.csv) |
| Ablation study | [`results/results of ablation study.csv`](results/results%20of%20ablation%20study.csv) |

Because GenLoc uses an LLM at temperature 1.0, individual re-runs are expected to
vary slightly from the published averages; the reduced scope demonstrates the
pipeline and metric computation rather than reproducing the exact table values.

### Claims supported / not supported by this artifact

* **Supported:** the end-to-end GenLoc localization pipeline (embedding-based
  retrieval + LLM-driven iterative exploration), the evaluation metrics
  (accuracy@k, MRR@10, MAP@10), and the precomputed ranked lists / result tables
  behind every table in the paper.
* **Not directly reproduced by a single command:** the exact averaged numbers in
  the comparison tables, which require three full trials across all projects of
  each dataset (long-running and dependent on live LLM responses). These are
  provided as precomputed CSVs under [`results/`](results/) and
  [`output-files/`](output-files/).
* **Baseline tools** (BugLocator, BLUiR, BRTracer, DreamLoc, CoSIL, LocAgent) are
  external and are not redistributed; their numbers are cited in the result
  tables.

## Documentation and layout

The GenLoc source, datasets, and per-trial outputs are described in the "Directory Structure" section above and in [`docs/implementation-and-default-configurations.md`](docs/implementation-and-default-configurations.md) and [`docs/time-cost-analysis.md`](docs/time-cost-analysis.md). The container entrypoint ([`docker/entrypoint.sh`](docker/entrypoint.sh)) dispatches to the run scripts in [`scripts/`](scripts/) (`run_smoke_test.sh`, `run_reduced.sh`,`run_full.sh`, `run_python_full.sh`).

---