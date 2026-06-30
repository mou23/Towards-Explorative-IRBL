# GenLoc (Java) — ISSTA 2026 artifact image.
# Builds a self-contained image for the GenLoc-Java pipeline on the Ye et al.
# dataset. The reduced-scope repository (tomcat) is cloned at build time so
# that no source code is downloaded during the experiments themselves.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    GIT_TERMINAL_PROMPT=0 \
    ANONYMIZED_TELEMETRY=False

# System dependencies:
#   git           -> required by PyDriller to checkout buggy commits
#   build-essential -> compiles C extensions (tree-sitter, chromadb deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        build-essential \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /artifact

# Install a CPU-only build of PyTorch first so that sentence-transformers does
# not pull in large CUDA wheels. This keeps the image smaller and GPU-free.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Python dependencies (pinned in the project's requirements file).
COPY source-code/GenLoc-Java/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Pre-bundle the reduced-scope repository. This build-time git clone is the ONLY
# place where source code is fetched from the network; the experiments run fully
# offline afterwards (apart from calls to the OpenAI API). It is placed before
# the source COPY so that editing the application code does not trigger a
# re-clone.
ARG REDUCED_REPO_URL=https://github.com/apache/tomcat
RUN git clone "$REDUCED_REPO_URL" /artifact/repos/tomcat

# Application source, dataset, helper scripts and entrypoint.
COPY source-code/GenLoc-Java /artifact/source-code/GenLoc-Java
COPY dataset/ye-et-al-dataset /artifact/dataset/ye-et-al-dataset
COPY scripts /artifact/scripts
COPY docker/entrypoint.sh /artifact/docker/entrypoint.sh

# Normalise line endings (in case the build host is Windows) and make scripts
# executable.
RUN sed -i 's/\r$//' /artifact/docker/entrypoint.sh /artifact/scripts/*.sh \
    && chmod +x /artifact/docker/entrypoint.sh /artifact/scripts/*.sh

VOLUME ["/artifact/output"]

ENTRYPOINT ["/artifact/docker/entrypoint.sh"]
CMD ["smoke"]
