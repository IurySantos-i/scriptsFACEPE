import csv
import ast
import math
from statistics import mean, stdev
import os
import glob

reps=["opengovernment","gitlabhq","quantified","wontomedia","bsmi","sequencescape","allourideas","openproject","one-click-orgs","action-center-platform","enroll","jekyll","diaspora","rapidftr","sharetribe","e-petitions","whitehall","otwarchive","Claim-for-Crown-Court-Defence"]



for rep in reps:
            def load_jekyll_data(jekyll_file):
                jekyll_data = {}
                with open(jekyll_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        task_id = row['Task']
                        jekyll_data[task_id] = {
                            'changed_files': set(row['Changed files'].strip('[]').replace("'", "").replace(' ', '').split(',')),
                            'testi': set(row['TestI'].strip('[]').replace("'", "").replace(' ', '').split(',')),
                            'testi_with_deps': set(row['TestIWithDeps'].strip('[]').replace("'", "").replace(' ', '').split(','))
                        }
                return jekyll_data

            def remove_duplicates(pairs):
                return list(dict.fromkeys(pairs))


            def process_pair_file(pair_file, jekyll_data):
                all_realpairs = []
                all_pairstesti = []
                all_pairstestiwithdeps = []
                processed_pairs = set()
                valid_pair_count = 0  # New counter for valid pairs

                # Create a set of task IDs to exclude
                exclude_tasks = {task for task, data in jekyll_data.items() if data['testi'] == data['testi_with_deps']}

                with open(pair_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        task = row['task']
                        if task in jekyll_data and task not in exclude_tasks:
                            pairs = ast.literal_eval(row['pairs'])
                            
                            # Filter out pairs that are in the exclude_tasks set
                            filtered_pairs = [pair for pair in pairs if str(pair) not in exclude_tasks and pair != int(task) and (task, str(pair)) not in processed_pairs]
                            
                            if filtered_pairs:
                                processed_pairs.update((task, str(pair)) for pair in filtered_pairs)
                                processed_pairs.update((str(pair), task) for pair in filtered_pairs)

                                task_data = jekyll_data[task]
                                for pair in filtered_pairs:
                                    if str(pair) in jekyll_data:
                                        pair_data = jekyll_data[str(pair)]
                                        
                                        changed_files_intersection = task_data['changed_files'].intersection(pair_data['changed_files'])
                                        all_realpairs.append(1 if changed_files_intersection else 0)
                                        
                                        testi_intersection = task_data['testi'].intersection(pair_data['testi'])
                                        all_pairstesti.append(1 if testi_intersection else 0)
                                        
                                        testi_with_deps_intersection = task_data['testi_with_deps'].intersection(pair_data['testi_with_deps'])
                                        all_pairstestiwithdeps.append(1 if testi_with_deps_intersection else 0)
                                        
                                        valid_pair_count += 1  # Increment the counter for each valid pair

                return all_realpairs, all_pairstesti, all_pairstestiwithdeps, valid_pair_count
            def calculate_metrics(all_realpairs, all_pairstesti, all_pairstestiwithdeps):
                tp_testi = sum(1 for a, b in zip(all_realpairs, all_pairstesti) if a == 1 and b == 1)
                fp_testi = sum(1 for a, b in zip(all_realpairs, all_pairstesti) if a == 0 and b == 1)
                fn_testi = sum(1 for a, b in zip(all_realpairs, all_pairstesti) if a == 1 and b == 0)
                
                tp_testi_deps = sum(1 for a, b in zip(all_realpairs, all_pairstestiwithdeps) if a == 1 and b == 1)
                fp_testi_deps = sum(1 for a, b in zip(all_realpairs, all_pairstestiwithdeps) if a == 0 and b == 1)
                fn_testi_deps = sum(1 for a, b in zip(all_realpairs, all_pairstestiwithdeps) if a == 1 and b == 0)
                
                testi_precision = tp_testi / (tp_testi + fp_testi) if (tp_testi + fp_testi) > 0 else 0
                testi_recall = tp_testi / (tp_testi + fn_testi) if (tp_testi + fn_testi) > 0 else 0
                testi_f2 = calculate_f2(testi_precision, testi_recall)
                
                testideps_precision = tp_testi_deps / (tp_testi_deps + fp_testi_deps) if (tp_testi_deps + fp_testi_deps) > 0 else 0
                testideps_recall = tp_testi_deps / (tp_testi_deps + fn_testi_deps) if (tp_testi_deps + fn_testi_deps) > 0 else 0
                testideps_f2 = calculate_f2(testideps_precision, testideps_recall)
                
                return {
                    'TestIPrecision': testi_precision,
                    'TestIRecall': testi_recall,
                    'TestIF2': testi_f2,
                    'TestIDepsPrecision': testideps_precision,
                    'TestIDepsRecall': testideps_recall,
                    'TestIDepsF2': testideps_f2
                }

            def calculate_f2(precision, recall):
                if precision + recall == 0:
                    return 0
                return 5 * (precision * recall) / (4 * precision + recall)

            def write_output(metrics, output_file, valid_pair_count):
                with open(output_file, 'w', newline='') as f:
                    fieldnames = ['Project', 'ValidPairCount', 'TestIPrecision', 'TestIRecall', 'TestIF2', 'TestIDepsPrecision', 'TestIDepsRecall', 'TestIDepsF2']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    row_data = {
                        'Project': os.path.basename(output_file).split('_')[0],
                        'ValidPairCount': valid_pair_count,
                        **{k: f"{v:.4f}" for k, v in metrics.items()}
                    }
                    writer.writerow(row_data)

            # Main execution
            jekyll_file = f'/home/iury/Downloads/Pares de tarefas do estudo original/Raw files/{rep}.csv'
            pair_file = f'/home/iury/Downloads/Pares de tarefas do estudo original/Pair files/{rep}.csv'
            output_file = f'/home/iury/Downloads/Pares de tarefas do estudo original/output/{rep}_output.csv'

            jekyll_data = load_jekyll_data(jekyll_file)
            all_realpairs, all_pairstesti, all_pairstestiwithdeps, valid_pair_count = process_pair_file(pair_file, jekyll_data)
            metrics = calculate_metrics(all_realpairs, all_pairstesti, all_pairstestiwithdeps)
            write_output(metrics, output_file, valid_pair_count)

            print(f"Output written to {output_file}")
