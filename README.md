# Towards Explorative IRBL: Combining Semantic Retrieval with LLM-driven Iterative Code Exploration
This paper proposes GenLoc, a novel IRBL technique that combines semantic retrieval with LLM-driven iterative code exploration to identify buggy files. It operates in two primary steps to localize relevant files. First, it retrieves a set of semantically similar files using an embedding-based similarity approach. Next, it employs an LLM augmented with a set of custom-designed code exploration functions, which enable the model to iteratively reason over the bug report and interact with the code base.

## 🗂️ Directory Structure

* `source-code/`: Contains the source code of GenLoc along with execution instructions.
* `output-files/`: Final ranked list produced by GenLoc (for each trial).
* `intermediate-files/`: Ranked list before applying post-processing (for each trial).
* `localized-bugs/`: Contains bugs correctly localized by GenLoc.
* `dataset/`: Contains XML files and GitHub URLs of the projects used for bug localization.
* `results/`: Contains the results of the experiments.
* `docs/`: Contains implementation details and time-cost analysis.
---
