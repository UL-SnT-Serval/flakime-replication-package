import pandas
import utils
import time
import os
import glob
import re
import numpy

CACHE_ORIGINAL = {}

def compute_reporting(row, threshold):
    if row['original_suspicion'] >= threshold and row['flaky_suspicion'] >= threshold:
        return 'TP'
    elif row['original_suspicion'] < threshold and row['flaky_suspicion'] >= threshold:
        return 'FP'
    elif  row['original_suspicion'] >= threshold and row['flaky_suspicion'] < threshold:
        return 'FN'
    elif row['original_suspicion'] < threshold and row['flaky_suspicion'] < threshold:
        return 'TN'
    elif numpy.isnan(row['original_suspicion']) or numpy.isnan(row['flaky_suspicion']):
        return ''
    else:
        raise RuntimeError('Unexpected combination original [{}] and flaky [{}] score for threshold {}'.format(row['original_suspicion'], row['flaky_suspicion'], threshold))


def compute_scores(data, threshold):
    reporting = data.apply(compute_reporting, axis=1, args=(threshold,))

    tp = reporting[reporting == 'TP'].size
    fp = reporting[reporting == 'FP'].size
    fn = reporting[reporting == 'FN'].size
    tn = reporting[reporting == 'TN'].size

    try:
        accuracy = (tp + tn) / (tp + tn + fp + fn)
    except ZeroDivisionError:
        accuracy = numpy.nan
        print('[ERROR]Division by Zero error when computing accuracy')

    try:    
        precision = tp / (tp + fp)
    except ZeroDivisionError:
        precision = numpy.nan
        print('[ERROR]Division by Zero error when computing precision')

    try:
        recall = tp / (tp + fn)
    except ZeroDivisionError:
        recall = numpy.nan
        print('[ERROR]Division by Zero error when computing recall')

    return accuracy, precision, recall


def get_original(path, project, bug_id, strategy, ranking):
    folder = utils.get_folder(path, project, bug_id, "0.00", strategy)
    file_name = os.path.join(folder, ranking + '-1.csv')
    
    if not file_name in CACHE_ORIGINAL:
        original = pandas.read_csv(file_name, sep=';').set_index('name')
        original.rename(columns={'suspiciousness_value': 'original_suspicion'}, inplace=True)
        CACHE_ORIGINAL[file_name] = original

    return CACHE_ORIGINAL[file_name]


def load_sbfl_file(path, file_name, project, bug_id, flake_rate, strategy, ranking):
    original = get_original(path, project, bug_id, strategy, ranking)
    data = pandas.read_csv(file_name, sep=';').set_index('name')
    data.rename(columns={'suspiciousness_value': 'flaky_suspicion'}, inplace=True)
    data = data.join(original, on='name')
    data.reset_index(inplace=True)
    data.drop(columns=['name'], inplace=True)

    return data


def load_sbfl(path, ranking, threshold):
    sbfl_data = []
    pattern = re.compile(ranking + '\-[0-9]+\.csv', re.IGNORECASE)

    for folder, project, bug_id, flake_rate, strategy in utils.walk_folders(path):
        files = utils.find_files(folder, pattern)
        project_id = '{}-{}'.format(project.capitalize(), bug_id)
        
        for file_name in files:
            data = load_sbfl_file(path, file_name, project, bug_id, flake_rate, strategy, ranking)
            [accuracy, precision, recall] = compute_scores(data, threshold)
            sbfl_data.append({'Bug ID': project_id, 'flake_rate': flake_rate, 'strategy': strategy, 'accuracy': accuracy, 'precision': precision, 'recall': recall})

    return pandas.DataFrame(sbfl_data)


def draw_sbfl(ranking, threshold):
    results = load_sbfl('data/sbfl', ranking, threshold)
    
    utils.lineplot(results, name='sbfl_accuracy',  x='flake_rate', y='accuracy', hue='Bug ID', y_label='Accuracy', x_label='Flakiness failure probability', fig_size=(6,5), legend_pos=None)
    utils.lineplot(results, name='sbfl_precision',  x='flake_rate', y='precision', hue='Bug ID', y_label='Precision', x_label='Flakiness failure probability', fig_size=(6,5), legend_pos=None)
    utils.lineplot(results, name='sbfl_recall',  x='flake_rate', y='recall', hue='Bug ID', y_label='Recall', x_label='Flakiness failure probability', fig_size=(6,5))

if __name__ == "__main__":
    ranking = 'ochiai'
    threshold = 0.1

    t_start = time.perf_counter()
    draw_sbfl(ranking, threshold)
    t_stop = time.perf_counter()

    print('\n')
    print("--------------------------------------------------")
    print('Elapsed time:{:.1f} [sec]'.format(t_stop-t_start))
    print("--------------------------------------------------") 