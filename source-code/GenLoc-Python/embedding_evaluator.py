import json
from datasets import load_dataset
from collections import defaultdict
from datetime import datetime

def extract_fixed_files(patch: str):
    files = set()
    for line in patch.splitlines():
        if line.startswith("diff --git"):
            parts = line.split()
            # diff --git a/foo/bar.py b/foo/bar.py
            file_path = parts[2][2:]  # remove "a/"
            files.add(file_path)
    return sorted(files)


def get_suspicious_files(file_path, top_n=50):
    with open(file_path, 'r') as file:
        parsed_data = json.load(file)
        parsed_data = parsed_data[0]

    files = [
        (parsed_data["metadata"][i]["file"], 1 - parsed_data["distance"][i])
        for i in range(len(parsed_data["metadata"]))
    ]
    sorted_files = sorted(files, key=lambda x: x[1], reverse=True)

    unique_files = {}
    for file, similarity in sorted_files:
        if file not in unique_files:
            unique_files[file] = similarity

    top_files = list(unique_files.items())[:top_n]

    return top_files


def calculate_accuracy_at_k(bug_data):
    for top in [1,5,10,50]:
        count = 0
        total_bug = 0
        for bug in bug_data:
            suspicious_files = bug['suspicious_files']
            # length_of_suspicious_files = len(suspicious_files)

            fixed_files = bug['fixed_files']

            # print(bug['bug_id'], fixed_files)
            for fixed_file in fixed_files:
                if fixed_file in suspicious_files[0:top]:
                    print(bug['bug_id'],fixed_file)
                    count = count + 1
                    break
            total_bug = total_bug + 1
        accuracy_percentage = (count * 100 / total_bug) if total_bug else 0
        print(f'accuracy@{top}: {accuracy_percentage:.0f}% ({count} out of {total_bug} bugs)')


def calculate_mean_reciprocal_rank_at_k(bug_data):
    for top in [10]:
        total_bug = 0
        inverse_rank = 0
        for bug in bug_data:
            suspicious_files = bug['suspicious_files']
            length_of_suspicious_files = len(suspicious_files)
            fixed_files = bug['fixed_files']
           
            # print("ID ",item['bug_id'])
            # print(suspicious_files)
            # print("length_of_suspicious_files",length_of_suspicious_files)
            minimum_length = min(top,length_of_suspicious_files)
            for i in range(minimum_length):
                if(suspicious_files[i] in fixed_files):
                    # print('first rank', item['bug_id'], i+1, suspicious_files[i])
                    inverse_rank = inverse_rank + (1/(i+1))
                    break
            total_bug = total_bug + 1
        if inverse_rank == 0:
            print("MRR@", top, 0)
        else:
            print("MRR@", top, (1/total_bug)*inverse_rank)
           
     
def calculate_mean_average_precision_at_k(bug_data):
    for top in [10]:
        total_bug = 0
        total_average_precision = 0
        for bug in bug_data:
            average_precision = 0
            precision = 0
            suspicious_files = bug['suspicious_files']
            length_of_suspicious_files = len(suspicious_files)
            fixed_files = bug['fixed_files']
            
            number_of_relevant_files = 0
            minimum_length = min(top,length_of_suspicious_files)
            for i in range(minimum_length):
                # print("i",i)
                if(suspicious_files[i] in fixed_files):
                    # print(item['bug_id'],suspicious_files[i], " relevant")
                    number_of_relevant_files = number_of_relevant_files + 1                        
                    precision = precision + (number_of_relevant_files/(i+1))
                # print("precision ", precision)
            average_precision = precision/len(fixed_files)
            # print("average_precision" ,average_precision, len(fixed_files))
            total_average_precision = total_average_precision + average_precision
            total_bug = total_bug + 1
        mean_average_precision = total_average_precision/total_bug
        print("MAP@", top, mean_average_precision)


def main():
    dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
    bug_data = []

    project_groups = defaultdict(list)
    for issue in dataset:
        project_name = issue['repo']
        project_groups[project_name].append(issue)

    for project, issues in project_groups.items():
        sorted_issues = sorted(issues, key=lambda x: datetime.fromisoformat(x['created_at'].replace('Z', '')))
        for issue in sorted_issues:
            print(issue['instance_id'], issue['base_commit'])
        
            suspicious_files = get_suspicious_files(project+'_bug_data/'+issue['instance_id']+'.json')

            bug_data_entry = {
                'bug_id': issue['instance_id'],
                'fixed_files': extract_fixed_files(issue["patch"]),
                'suspicious_files': [file for file, _ in suspicious_files]
            }
            bug_data.append(bug_data_entry)

    calculate_accuracy_at_k(bug_data)
    calculate_mean_reciprocal_rank_at_k(bug_data)
    calculate_mean_average_precision_at_k(bug_data)
    
if __name__ == "__main__":
    main()