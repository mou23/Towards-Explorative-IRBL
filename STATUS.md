# STATUS

## Badge(s) applied for

* **Artifacts Available** 
* **Artifacts Evaluated - Functional**

## Justification

### Artifacts Available

The artifact is:

* **Publicly accessible** — the complete replication package (source code of the
  GenLoc-Java and GenLoc-Python pipelines, bug-report datasets, precomputed
  per-trial output files, localized-bug lists, and the result tables that back
  the paper's claims) is archived in a public repository with a permanent
  identifier.
* **Self-described and packaged** — it ships with a `README` (Getting Started +
  step-by-step reproduction), a `REQUIREMENTS` file, this `STATUS` file, and an
  open-source `LICENSE` (MIT).
* **Containerized for convenience** — `Dockerfile.java`, `Dockerfile.python`, and
  `docker-compose.yml` are provided so the artifact can be inspected and run
  without manual dependency installation.

### Artifacts Evaluated — Functional

The artifact is **documented, consistent, complete, and exercisable**:

* **Documented** — the `README` provides a Getting Started guide and
  step-by-step reproduction instructions, supported by `REQUIREMENTS.md` and
  the `docs/` notes; every result table in the paper is mapped to its file in
  `results/` and `output-files/`.
* **Consistent and complete** — the source code, datasets, run scripts, and
  containers together reproduce the GenLoc pipeline (embedding-based retrieval +
  LLM-driven exploration) and its evaluation metrics (accuracy@k, MRR@10,
  MAP@10) that underpin the paper's claims.
* **Exercisable** — a containerized environment with a ~30-minute "smoke test"
  and a reduced-scope experiment (completes in well under one day) lets
  reviewers run the end-to-end pipeline and verify metric computation. An OpenAI
  API key has been provided to the committee for this purpose.

Because GenLoc uses an LLM at temperature 1.0, individual re-runs vary slightly
from the published three-trial averages; the smoke and reduced scopes
demonstrate functionality and metric computation, while the precomputed CSVs
back the exact table values.
