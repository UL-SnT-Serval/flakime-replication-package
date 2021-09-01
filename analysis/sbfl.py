import pandas
import utils
import time
import os
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
    if not utils.is_cached('sbfl'):
        sbfl_data = []
        pattern = re.compile(ranking + '\-[0-9]+\.csv', re.IGNORECASE)

        for folder, project, bug_id, flake_rate, strategy in utils.walk_folders(path):
            files = utils.find_files(folder, pattern)
            project_id = '{}-{}'.format(project.capitalize(), bug_id)
            
            for file_name in files:
                data = load_sbfl_file(path, file_name, project, bug_id, flake_rate, strategy, ranking)
                [accuracy, precision, recall] = utils.compute_scores(data, lambda x: compute_reporting(x, threshold))
                sbfl_data.append({'Bug ID': project_id, 'flake_rate': float(flake_rate), 'strategy': strategy, 'accuracy': accuracy, 'precision': precision, 'recall': recall})

        utils.store_file_in_cache(pandas.DataFrame(sbfl_data), 'sbfl')

    return utils.load_cache('sbfl')


def draw_sbfl(ranking, threshold):
    results = load_sbfl('data/sbfl', ranking, threshold)
    results['Bug ID'] = results['Bug ID'].str.lower()
    print(results)
    
    data =results.groupby(['Bug ID', 'flake_rate', 'strategy'], as_index=False).mean()
    data = data.loc[data['flake_rate'].isin([0.00,0.2])]
    print(data)

    utils.lineplot(results, name='sbfl_accuracy',  x='flake_rate', y='accuracy', hue='Bug ID', y_label='Accuracy', x_label='Nominal Flake Rate', fig_size=(6,5), legend_pos=None)
    utils.lineplot(results, name='sbfl_precision',  x='flake_rate', y='precision', hue='Bug ID', y_label='Precision', x_label='Nominal Flake Rate', fig_size=(6,5), legend_pos=None)
    utils.lineplot(results, name='sbfl_recall',  x='flake_rate', y='recall', hue='Bug ID', y_label='Recall', x_label='Nominal Flake Rate', fig_size=(6,5))

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