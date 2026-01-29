# Towards Explorative IRBL: Combining Semantic Retrieval with LLM-driven Iterative Code Exploration
This paper proposes GenLoc, a novel IRBL technique that combines semantic retrieval with LLM-driven iterative code exploration to identify buggy files. It operates in two primary steps to localize relevant files. First, it retrieves a set of semantically similar files using an embedding-based similarity approach. Next, it employs an LLM augmented with a set of custom-designed code exploration functions, which enable the model to iteratively reason over the bug report and interact with the code base.

## 🗂️ Directory Structure

* `source_code/`: Contains the source code of GenLoc.
* `output_files/`: Ranked list produced by GenLoc (for each trial).
* `localized_bugs/`: Contains bugs correctly localized by GenLoc.
* `ghrb_dataset/` and `ye_et_al_dataset/`: Contains XML files and GitHub URLs of the projects used for bug localization.
* `results/`: Contains the results of the experiments
---

## ⚙️ Set-Up

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Place your OpenAI API key in a file named `api_key.txt` in the project root directory.

---

## 🔧 How to Run

To run GenLoc, first navigate to the source code directory:

```bash
cd source_code
```

Then, execute the following steps:

```bash
# Step 1: Execute embedding-based retrieval
# Format: python main.py <project_name> <project_repo_path> <bug_report_xml> <embedding_model>
# Example:
python main.py aspectj ye_et_al_dataset/aspectj ye_et_al_dataset/aspectj.xml openai

# Step 2: Run the LLM-based analysis
# Format: python bug_localizer.py <project_name> <bug_report_xml>
# Example:
python bug_localizer.py aspectj ye_et_al_dataset/aspectj.xml

# Step 3: Perform post-processing
# Format: python post_processor.py <project_name>
# Example:
python post_processor.py aspectj

# Step 4: Evaluate performance using standard metrics
# Format: python evaluation_metric_calculator.py <project_name>
# Example:
python evaluation_metric_calculator.py aspectj
```

---
