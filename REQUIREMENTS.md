# REQUIREMENTS

This document describes the hardware and software requirements to build and run
the GenLoc artifact.

## Architecture

* **CPU architecture:** x86-64 (amd64). The images use the `python:3.11-slim`
  base and CPU-only PyTorch wheels; no GPU is required.
* Apple Silicon / ARM hosts can run the images through emulation
  (`--platform linux/amd64`) but this is slower and not the tested path.

## Software requirements

* **Docker Engine 20.10+** (or Podman 4+) with the Compose v2 plugin
  (`docker compose ...`). The artifact was packaged and tested with Docker.
* Internet access is required:
  * **at build time** — to install Python dependencies and to clone the bundled
    `tomcat` repository;
  * **at run time** — only for calls to the **OpenAI API** (chat + embeddings).
    The GenLoc-Java reduced/smoke scope performs no other network access.
  * The **GenLoc-Python** (SWE-bench Lite) full scope additionally downloads the
    dataset from the Hugging Face Hub and clones 12 repositories at run time.
* **OpenAI API key** with access to `gpt-4o-mini` and `text-embedding-3-small`.
  Reviewers supply their own key via the `OPENAI_API_KEY` environment variable
  or by mounting a file to `/artifact/source-code/api_key.txt`.
  Approximate cost: ~US$0.01 per bug (Ye et al.), ~US$0.02–0.03 per bug
  (GHRB / SWE-bench Lite).

## Hardware requirements

* **RAM:** 8 GB recommended (4 GB minimum) for the Java reduced/smoke scope.
* **Disk:**
  * GenLoc-Java image: ~7–10 GB (Python + CPU PyTorch + bundled `tomcat` clone).
  * GenLoc-Python full scope: an additional ~15–25 GB for the 12 SWE-bench
    repositories cloned at run time.
* **No non-commodity peripherals** are required.

## Machine-readable dependency descriptions

* [`Dockerfile.java`](Dockerfile.java) — GenLoc-Java image definition.
* [`Dockerfile.python`](Dockerfile.python) — GenLoc-Python image definition.
* [`docker-compose.yml`](docker-compose.yml) — service/build orchestration.
* [`source-code/GenLoc-Java/requirements.txt`](source-code/GenLoc-Java/requirements.txt)
  and
  [`source-code/GenLoc-Python/requirements.txt`](source-code/GenLoc-Python/requirements.txt)
  — pinned Python dependencies.

## Estimated runtimes

* **Smoke test** (1 bug, tomcat): a few minutes (dominated by the initial
  repository checkout and embedding of the first commit).
* **Reduced experiment** (10 bugs, tomcat): well under 30 mins.
* **Full per-project experiment**: scales with the number of bugs
  (~47 s/bug on average plus per-version embedding); the largest projects can
  take several hours to a day.
