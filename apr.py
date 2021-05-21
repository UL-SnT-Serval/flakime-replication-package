import pandas
import utils
import re
import time
import os
import glob
import numpy

from scipy.stats import mannwhitneyu

def get_strategy(input):
    if input == 'vocabulary':
        return 'non-targeted'
    elif input == 'vocabulary-no-fl':
        return 'targeted'

    return input


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

        arja_data.append({'Project': project, 'Bug ID': bug_name, 'Strategy': get_strategy(strategy), 'Flake Rate': float(flake_rate), 'Total Tests': total, 'Positive Tests': positive, 'Negative Tests': negative, 'Successful Tests': success, 'Failed Tests': failed, 'Valid Patches': valid_patches[repetition]})

    return arja_data


def load_arja(path):
    arja_data = []

    for folder, project, bug_id, flake_rate, strategy in utils.walk_folders(path):
        data = get_arja_data(folder, project, bug_id, flake_rate, strategy)
        arja_data.extend(data)

    return pandas.DataFrame(arja_data)


def print_arja_statistics(data):
    print("--------------------------------------------------")
    print('ARJA statistics: loss of valid patches')
    print("--------------------------------------------------")
    data_vocabulary = data.loc[data['Strategy'] == 'non-targeted']
    compare_loss = data_vocabulary.loc[data_vocabulary['Flake Rate'].isin([0.0, 0.05])].groupby(['Bug ID', 'Flake Rate'])['Valid Patches'].mean().unstack()
    compare_loss['loss [%]'] = compare_loss.apply(lambda row: (row[0.05] - row[0.00]) / row[0.00] * 100, axis=1)
    print(compare_loss)

    print("--------------------------------------------------")
    print('ARJA statistics: wilcoxon of targeted vs non-targeted')
    print("--------------------------------------------------")
    wicloxon_targeted = []
    for bug_id in data['Bug ID'].unique():
        non_targeted = data.loc[(data['Flake Rate'] == 0.05) & (data['Strategy'] == 'non-targeted') & (data['Bug ID'] == bug_id)]['Valid Patches']
        targeted = data.loc[(data['Flake Rate'] == 0.05) & (data['Strategy'] == 'targeted') & (data['Bug ID'] == bug_id)]['Valid Patches']
        w, p = mannwhitneyu(non_targeted, targeted)
        wicloxon_targeted.append({'Bug ID': bug_id, 'p-value': p, 'significant': p < 0.05}) 
    print(pandas.DataFrame(wicloxon_targeted))

    print("--------------------------------------------------")
    print('ARJA statistics: increase when non-targeted')
    print("--------------------------------------------------")
    data_targeted = data.loc[data['Flake Rate'] == 0.05].groupby(['Bug ID', 'Strategy'])['Valid Patches'].mean().unstack()
    data_targeted['gain [%]'] = data_targeted.apply(lambda row: (row['targeted'] - row['non-targeted']) / row['non-targeted'] * 100, axis=1)
    print(data_targeted)

def draw_arja(data):
    data_vocabulary = data.loc[data['Strategy'] == 'non-targeted']
    utils.lineplot(data_vocabulary, 'arja_valid_patches', 'Flake Rate', 'Valid Patches', 'Bug ID', y_label='Number of valid patches', x_label='Nominal Flake Rate', x_lim=[0,0.2], fig_size=(6,5))
    utils.lineplot(data_vocabulary, 'arja_total_tests', 'Flake Rate', 'Total Tests', 'Bug ID', y_label='Number of tests executed', x_label='Nominal Flake Rate', x_lim=[0,0.2], y_lim=[0,800], fig_size=(6,5))
    utils.lineplot(data_vocabulary, 'arja_failing_tests', 'Flake Rate', 'Negative Tests', 'Bug ID', y_label='Number of tests executed', x_label='Nominal Flake Rate', x_lim=[0,0.2], y_lim=[0,200], fig_size=(6,5), legend_pos=None)
    utils.lineplot(data_vocabulary, 'arja_passing_tests', 'Flake Rate', 'Positive Tests', 'Bug ID', y_label='Number of tests executed', x_label='Nominal Flake Rate', x_lim=[0,0.2], y_lim=[0,800], fig_size=(6,5), legend_pos=None)

    data_0_05 = data.loc[data['Flake Rate'] == 0.05]  
    utils.boxplot(data_0_05, 'arja_no_fl', 'Bug ID', 'Valid Patches', y_label='Number of valid patches', hue='Strategy')


if __name__ == "__main__":
    t_start = time.perf_counter()
    arja_data = load_arja('data/apr/arja')
    print_arja_statistics(arja_data)
    draw_arja(arja_data)
    t_stop = time.perf_counter()

    print('\n')
    print("--------------------------------------------------")
    print('Elapsed time:{:.1f} [sec]'.format(t_stop-t_start))
    print("--------------------------------------------------") 