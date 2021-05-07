import pandas
import utils
import re
import time
import os
import glob
import numpy

def get_digit(line):
    return [int(s) for s in line.split() if s.isdigit()][0]


def list_dirs(path):
    return [(os.path.join(os.path.join(path,dI)), dI) for dI in os.listdir(path) if os.path.isdir(os.path.join(path,dI))]


def find_dirs(path, regex):
    return [f for f in list_dirs(path) if re.match(regex, f[1])]


def list_files(path):
    return [(os.path.join(os.path.join(path,dI)), dI) for dI in os.listdir(path) if os.path.isfile(os.path.join(path,dI))]


def find_files(path, regex):
    return [f[0] for f in list_files(path) if re.match(regex, f[1])]


def get_valid_patches(folder, repetitions):
    patches = numpy.zeros(repetitions)

    dirs = find_dirs(folder, r'patch*')
    for index, patch_dir in enumerate(dirs):
        number_patches = len(find_files(patch_dir[0], r'Patch*'))
        patches[index] = number_patches

    return patches.astype(int)


def get_value(file, regex):
    value = numpy.nan
    
    with open(file) as fp:
        for line in fp:
            if re.match(regex,line):
                if numpy.isnan(value):
                    value = 0

                value = value + get_digit(line)
    
    return value


def extract_arja_log_statistics(file):
    positive = get_value(file, r'Number of positive tests:\s+\d+')
    negative = get_value(file, r'Number of negative tests:\s+\d+')
    success = get_value(file, r'Success\s+=\s+\d+')
    failed = get_value(file, r'Failed \(\w+\)\s+=\s+\d+')

    return (positive, negative, success, failed)


def get_arja_data(folder, project, bug_id, flake_rate, strategy):
    bug_name = "{}-{}".format(project, bug_id)
    
    arja_data = []
    
    repetitions = len(glob.glob1(folder,"*.log"))
    valid_patches = get_valid_patches(folder, repetitions)

    for repetition in range(0, repetitions):
        arja_log = os.path.join(folder, "{}_{}_{}_{}_{}.log".format(project, bug_id, flake_rate, strategy, repetition + 1))
        positive, negative, success, failed = extract_arja_log_statistics(arja_log)
        total = positive + negative

        arja_data.append({'Project': project, 'Bug ID': bug_name, 'Strategy': strategy, 'Flake Rate': flake_rate, 'Total Tests': total, 'Positive Tests': positive, 'Negative Tests': negative, 'Successful Tests': success, 'Failed Tests': failed, 'Valid Patches': valid_patches[repetition]})

    return arja_data


def load_arja(path):
    arja_data = []

    for project_dir, project in list_dirs(path):
        for bug_id_dir, bug_id in list_dirs(project_dir):
            for flake_rate_dir, flake_rate in list_dirs(bug_id_dir):
                for strategy_dir, strategy in list_dirs(flake_rate_dir):
                    data = get_arja_data(strategy_dir, project, bug_id, float(flake_rate), strategy)
                    arja_data.extend(data)

    return pandas.DataFrame(arja_data)


def draw_arja():
    data = load_arja('data/apr/arja')

    for strategy in data['Strategy'].unique():
        data_strategy = data.loc[data['Strategy'] == strategy]
        print(data_strategy)
        utils.lineplot(data_strategy, 'arja_all_valid_patches_' + strategy, 'Flake Rate', 'Valid Patches', 'Bug ID', y_label='Number of valid patches', x_label='Flaky Failure Rate', x_lim=[0,0.5])
        utils.lineplot(data_strategy, 'arja_all_total_tests_' + strategy, 'Flake Rate', 'Total Tests', 'Bug ID', y_label='Number of tests executed', x_label='Flaky Failure Rate', x_lim=[0,0.5])
        utils.lineplot(data_strategy, 'arja_all_failing_tests_' + strategy, 'Flake Rate', 'Failed Tests', 'Bug ID', y_label='Number of tests executed', x_label='Flaky Failure Rate', x_lim=[0,0.5])
        utils.lineplot(data_strategy, 'arja_all_passing_tests_' + strategy, 'Flake Rate', 'Positive Tests', 'Bug ID', y_label='Number of tests executed', x_label='Flaky Failure Rate', x_lim=[0,0.5])

if __name__ == "__main__":
    t_start = time.perf_counter()
    draw_arja()
    t_stop = time.perf_counter()

    print('\n')
    print("--------------------------------------------------")
    print('Elapsed time:{:.1f} [sec]'.format(t_stop-t_start))
    print("--------------------------------------------------") 