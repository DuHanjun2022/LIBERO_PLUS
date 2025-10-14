import os
from pprint import pprint

task_suite = "custom_eval_easy"
task_suite = "libero_10_random"

path = os.path.join("/home/leisongao/LIBERO/libero/libero/bddl_files/", task_suite)

files = os.listdir(path)
out = []
for f in files:
    out.append(f[:-5])

pprint(out)