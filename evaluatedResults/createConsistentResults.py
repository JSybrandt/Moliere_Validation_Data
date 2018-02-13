#!/usr/bin/env python3
import os
import os.path

file_names = [
        "{}.path.eval",
        "{}.twe.eval",
        "{}.tpw.eval",
        "{}.cos.eval",
        "{}.l2.eval",
        "{}.hybrid.eval"
]

trial_names = [
    "fake",
    "real",
    "highlyCited"
]

for trial in trial_names:
    finished_runs = set()
    first_run = True

    # populate finished_runs
    for file_template in file_names:
        file_name = file_template.format(trial)
        print("Reading", file_name)
        with open(file_name) as file:
            local_runs = set()
            for line in file:
                c1, c2, _ = line.split(" ", 2)
                if c2 > c1:
                    c1, c2 = c2, c1
                local_runs.add("{}{}".format(c1, c2))
            if first_run:
                finished_runs = local_runs
                first_run = False
            else:
                finished_runs = finished_runs.intersection(local_runs)
            print("Found", len(local_runs), "runs")
            print("Intersection Size:", len(finished_runs))

    tmp_dir = os.path.join(os.getcwd(), "tmp")
    try:
        os.mkdir(tmp_dir)
    except:
        print("tmp dir already exists")

    # rewrite with subset
    for file_template in file_names:
        in_file_name = file_template.format(trial)
        out_file_name = os.path.join(tmp_dir, in_file_name)
        print("Writing", out_file_name)
        with open(in_file_name) as in_file, open(out_file_name, 'w') as out_file:
            for line in in_file:
                c1, c2, _ = line.split(" ", 2)
                if c2 > c1:
                    c1, c2 = c2, c1
                key = "{}{}".format(c1, c2)
                if key in finished_runs:
                    out_file.write(line)

