import numpy as np
import utils
import os
import pandas as pd
import time


def compute_difference(row, df):
    return row['Mutation Score'] - df[(df['Bug ID'] == row['Bug ID']) & (df['Strategy'] == row['Strategy'])].iloc[0]['Mutation Score']


def get_mutation_data(folder, project, bug_id, flake_rate, strategy):
    mutation_log = os.path.join(folder, 'output.out')

    data = pd.read_csv(mutation_log, header=None, names=["repetition", "Mutants", "Flakes", "Killed"])
    data.drop('repetition', axis="columns", inplace=True)
    data['Mutation Score'] = (data["Killed"] / data["Mutants"]) * 100
    data['Flake Rate'] = float(flake_rate)
    data['Strategy'] = strategy
    data['Bug ID'] = "{}-{}".format(project, bug_id)
    data['Project'] = project

    return data


def load_mutation(path):
    mutation_data = pd.DataFrame()

    for folder, project, bug_id, flake_rate, strategy in utils.walk_folders(path):
        data = get_mutation_data(folder, project, bug_id, flake_rate, strategy)
        mutation_data = mutation_data.append(data)

    mutation_data.reset_index(drop=True, inplace=True)

    mutation_data['Difference'] = mutation_data.apply(lambda x: compute_difference(x, mutation_data), axis='columns')

    return mutation_data

def draw_mutation(data):
    utils.lineplot(data, name='mutation_score', x='Flake Rate', y='Mutation Score', y_label='$\overline{MS}$ [%]', hue='Project', x_label='Nominal Flake Rate', y_lim=[0, 100])

    std = data.groupby(['Project', 'Bug ID', 'Flake Rate', 'Strategy'])['Mutation Score'].agg(np.std, ddof=1).reset_index()
    utils.lineplot(std, name='mutation_std', x='Flake Rate', y='Mutation Score', y_label='Standard Deviation [%]', hue='Project', x_label='Nominal Flake Rate')
    
    displayed = data.loc[data['Flake Rate'].isin(np.arange(0.00, 0.501, 0.05))].copy()
    utils.boxplot(displayed, name='mutation_sampled_difference', x='Flake Rate', y='Difference', y_label='Difference [%]', hue='Project', x_label='Nominal Flake Rate' )


if __name__ == "__main__":
    t_start = time.perf_counter()
    data = load_mutation('../data/mutation')
    draw_mutation(data)
    t_stop = time.perf_counter()

    print('\n')
    print("--------------------------------------------------")
    print('Elapsed time:{:.1f} [sec]'.format(t_stop-t_start))
    print("--------------------------------------------------") 
