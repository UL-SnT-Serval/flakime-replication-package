import pandas
import utils
import re
import time
import os
import glob
import numpy

def get_digit(line):
    return [int(s) for s in line.split() if s.isdigit()][0]


def get_valid_patches(folder, repetitions):
    patches = numpy.zeros(repetitions)

    dirs = utils.find_dirs(folder, r'patch*')
    for index, patch_dir in enumerate(dirs):
        number_patches = len(utils.find_files(patch_dir[0], r'Patch*'))
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
    positive = get_value(file, r'Number of positive tests considered:\s+\d+')
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

        arja_data.append({'Project': project, 'Bug ID': bug_name, 'Strategy': strategy, 'Flake Rate': float(flake_rate), 'Total Tests': total, 'Positive Tests': positive, 'Negative Tests': negative, 'Successful Tests': success, 'Failed Tests': failed, 'Valid Patches': valid_patches[repetition]})

    return arja_data


def load_arja(path):
    arja_data = []

    for folder, project, bug_id, flake_rate, strategy in utils.walk_folders(path):
        data = get_arja_data(folder, project, bug_id, flake_rate, strategy)
        arja_data.extend(data)

    return pandas.DataFrame(arja_data)


def draw_arja():
    data = load_arja('data/apr/arja')

    data_vocabulary = data.loc[data['Strategy'] == 'vocabulary']
    utils.lineplot(data_vocabulary, 'arja_all_valid_patches', 'Flake Rate', 'Valid Patches', 'Bug ID', y_label='Number of valid patches', x_label='Flaky Failure Rate', x_lim=[0,0.5])
    utils.lineplot(data_vocabulary, 'arja_all_total_tests', 'Flake Rate', 'Total Tests', 'Bug ID', y_label='Number of tests executed', x_label='Flaky Failure Rate', x_lim=[0,0.5])
    utils.lineplot(data_vocabulary, 'arja_all_failing_tests', 'Flake Rate', 'Failed Tests', 'Bug ID', y_label='Number of tests executed', x_label='Flaky Failure Rate', x_lim=[0,0.5])
    utils.lineplot(data_vocabulary, 'arja_all_passing_tests', 'Flake Rate', 'Positive Tests', 'Bug ID', y_label='Number of tests executed', x_label='Flaky Failure Rate', x_lim=[0,0.5])

    data_0_05 = data.loc[data['Flake Rate'] == 0.05]
    utils.boxplot(data_0_05, 'arja_no_fl', 'Bug ID', 'Valid Patches', y_label='Number of valid patches', hue='Strategy')


if __name__ == "__main__":
    t_start = time.perf_counter()
    draw_arja()
    t_stop = time.perf_counter()

    print('\n')
    print("--------------------------------------------------")
    print('Elapsed time:{:.1f} [sec]'.format(t_stop-t_start))
    print("--------------------------------------------------") 