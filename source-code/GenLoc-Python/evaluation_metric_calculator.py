import csv
import json
import os

def parse_json(json_data):
    try:
        data = json.loads(json_data)
        file_names = [item["file"] for item in data["ranked_list"]]
        return file_names
    except json.JSONDecodeError:
        return []
    except KeyError:
        return []

def ensure_list(x):
    if isinstance(x, str):
        import ast
        return ast.literal_eval(x)
    return x

def process_bug_results(csv_path, project_name):
    bug_results = {}
    with open(csv_path, newline='', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bug_id = row['bug_id']
            try:
                if not row['fixed_files']:
                    print(f"Warning: Fixed files missing for {bug_id}. Skipping.")
                    continue
                bug_id = f"{bug_id}"
                suspicious_files = parse_json(row['suspicious_files'])
                fixed_files = ensure_list(row['fixed_files'])
                # print(type(fixed_files))
                bug_results[bug_id] = {
                    'suspicious_files': suspicious_files,
                    'fixed_files': fixed_files
                }
                
            except Exception as e:
                print(e)
                
    return bug_results

def calculate_metrics(bug_results):
    total_bugs = len(bug_results)
    print(f"\nTotal Bugs Processed: {total_bugs}")

    # Accuracy@k
    for top in [1, 5, 10]:
        count = 0
        for bug_id, result in bug_results.items():
            suspicious_files = result['suspicious_files']
            fixed_files = result['fixed_files']
            
            for fixed_file in fixed_files:
                
                if fixed_file in suspicious_files[:top]:
                    # print(bug_id,fixed_file)
                    count += 1
                    break
        accuracy_percentage = (count * 100 / total_bugs) if total_bugs else 0
        print(f'accuracy@{top}: {accuracy_percentage:.0f}% ({count} out of {total_bugs} bugs)')

    # MRR@10
    inverse_rank = 0
    for bug_id, result in bug_results.items():
        suspicious_files = result['suspicious_files']
        fixed_files = result['fixed_files']
        minimum_length = min(10, len(suspicious_files))
        for i in range(minimum_length):
            if suspicious_files[i] in fixed_files:
                inverse_rank += 1 / (i + 1)
                break
    mrr = inverse_rank / total_bugs if total_bugs != 0 else 0
    print(f"MRR@10: {mrr:.4f}")

    # MAP@10
    total_average_precision = 0
    for bug_id, result in bug_results.items():
        suspicious_files = result['suspicious_files']
        fixed_files = result['fixed_files']
        precision = 0
        number_of_relevant_files = 0
        minimum_length = min(10, len(suspicious_files))
        for i in range(minimum_length):
            if suspicious_files[i] in fixed_files:
                number_of_relevant_files += 1
                precision += number_of_relevant_files / (i + 1)
        if len(fixed_files) != 0:
            average_precision = precision / len(fixed_files)
            total_average_precision += average_precision
    map_k = total_average_precision / total_bugs if total_bugs != 0 else 0
    print(f"MAP@10: {map_k:.4f}")

if __name__ == "__main__":
    root_dir = '.'

    all_bug_results = {}

    for root, _, files in os.walk(root_dir):
        for file_name in files:
            if file_name.endswith('_final_ranked_output.csv'):
                project_name = file_name.replace('_final_ranked_output.csv', '')
                csv_path = os.path.join(root, file_name)
                # print(f"Processing project: {project_name}")
                project_bug_results = process_bug_results(csv_path, project_name)
                # print(project_bug_results)
                all_bug_results.update(project_bug_results)

    calculate_metrics(all_bug_results)