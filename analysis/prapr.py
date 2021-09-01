import numpy as np
import utils
import os
import pandas as pd
import time

def get_prapr_data(folder, project, bug_id, flake_rate, strategy):
    mutation_log = os.path.join(folder, "{}_{}_{}_{}.log".format(project, bug_id, flake_rate, strategy))

    data = pd.read_csv(mutation_log, header=None, names=["Patches"])
    data['Flake Rate'] = float(flake_rate)
    data['Strategy'] = strategy
    data['Bug ID'] = "{}-{}".format(project, bug_id)
    data['Project'] = project

    return data


def load_prapr(path):
    mutation_data = pd.DataFrame()

    for folder, project, bug_id, flake_rate, strategy in utils.walk_folders(path):
        data = get_prapr_data(folder, project, bug_id, flake_rate, strategy)
        mutation_data = mutation_data.append(data)

    mutation_data.reset_index(drop=True, inplace=True)

    return mutation_data


def draw_prapr(data):
    data_math = data.loc[data['Project'] == 'math']
    utils.lineplot(data_math, name='prapr_valid_math', x='Flake Rate', y='Patches', y_label='Number of valid patches', hue='Bug ID', x_label='Nominal Flake Rate')

    data_chart = data.loc[data['Project'] == 'chart']
    utils.lineplot(data_chart, name='prapr_valid_chart', x='Flake Rate', y='Patches', y_label='Number of valid patches', hue='Bug ID', x_label='Nominal Flake Rate')

    data_others = data.loc[~data['Project'].isin(['chart', 'math'])]
    utils.lineplot(data_others, name='prapr_valid_others', x='Flake Rate', y='Patches', y_label='Number of valid patches', hue='Bug ID', x_label='Nominal Flake Rate')


if __name__ == "__main__":
    t_start = time.perf_counter()
    data = load_prapr('../data/apr/prapr')
    draw_prapr(data)
    t_stop = time.perf_counter()

    print('\n')
    print("--------------------------------------------------")
    print('Elapsed time:{:.1f} [sec]'.format(t_stop-t_start))
    print("--------------------------------------------------") 
