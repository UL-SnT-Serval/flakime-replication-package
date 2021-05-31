import numpy as np
import yaml
import utils
import os
import pandas as pd


def load_mutation(path, proba, project_name, rep, initial):
    res = pd.read_csv(path, header=None, names=["rep", "mutant", "flakes", "killed"])
    print(f"{project_name} : {proba}")
    mutation_scores = (res["killed"] / res["mutant"]) * 100
    res["score"] = mutation_scores
    res["probability"] = np.repeat(proba, rep)
    res["project"] = np.repeat(project_name, rep)
    res["difference"] = res['score'] - initial * 100

    res.drop('rep', axis="columns", inplace=True)
    return res


def load_prapr(path, proba, project_name, rep, patches):
    res = pd.read_csv(path, header=None, names=["valid"])
    print(f"{project_name} : {proba}")
    res["patches"] = np.repeat(patches, rep)
    res["probability"] = np.repeat(proba, rep)
    res["project"] = np.repeat(project_name, rep)
    # res.drop('rep', axis="columns", inplace=True)
    return res


def get_config(config_path=None):
    with open(config_path, "r") as config_file:
        c = yaml.safe_load(config_file)
    return c


def main_mutation():
    config = get_config("config_pit.yml")
    res = None
    res_describe = None
    for (proj, cfg) in config["dataset"].items():
        project_values= None
        for (fr, rep) in cfg["flakerates"].items():
            values = load_mutation(f"{cfg['path']}/output_{fr}.out", fr, proj, rep, cfg['initial'])
            values["std"] = values["score"].std()
            values_describe = pd.DataFrame(values["score"].describe().drop("count")).T
            values_describe["project"] = proj
            values_describe["fr"] = fr
            cols = values_describe.columns.tolist()
            cols = cols[-2:] + cols[:-2]
            values_describe = values_describe[cols]
            if project_values is None:
                project_values = values_describe
            else:
                project_values = project_values.append(values_describe, ignore_index=True, sort=False)

            if res is None:
                res = values
            else:
                res = res.append(values, ignore_index=True, sort=False)
        project_values["std_mean"] = project_values["std"].mean()
        if res_describe is None:
            res_describe = project_values
        else:
            res_describe = res_describe.append(project_values, ignore_index=True, sort=False)

    res_describe = res_describe.loc[res_describe["fr"].isin([0, 0.1, 0.2, 0.3, 0.4, 0.5])]

    res_describe.to_csv(path_or_buf="df_mutation.csv", index=False)
    # res["std"] = res["score"].std()

    utils.lineplot(res, name='mutation_score', x='probability', y='score', y_label='$\overline{MS}$ [%]', hue='project',
                    x_label='Nominal Flake Rate', y_lim=[0, 100])
    utils.lineplot(res, name='mutation_std', x='probability', y='std', y_label='Standard Deviation [%]', hue='project',
                    x_label='Nominal Flake Rate')
    # displayed = res.loc[res['probability'].isin(np.arange(0.00, 0.501, 0.05))].copy()
    displayed = res.loc[res['probability'] > 0.09]
    utils.boxplot(displayed, name='mutation_sampled_difference', x='probability', y='difference', y_label='Difference [%]', hue='project',
                  x_label='Nominal Flake Rate' )


def main_prapr():
    config = get_config("config_prapr.yml")
    res = None
    res_describe = None
    for (proj, cfg) in config["project"].items():
        for (fr, rep) in cfg["flakerates"].items():
            values = load_prapr(f"{cfg['path']}/{fr}.log", fr, proj, rep, cfg['n_patches'])
            values["std"] = values["valid"].std()
            values_describe = pd.DataFrame(values["valid"].describe().drop("count")).T
            values_describe["project"] = proj
            values_describe["fr"] = fr
            cols = values_describe.columns.tolist()
            cols = cols[-2:] + cols[:-2]
            values_describe = values_describe[cols]
            if res_describe is None:
                res_describe = values_describe
            else:
                res_describe = res_describe.append(values_describe, ignore_index=True, sort=False)
            if res is None:
                res = values
            else:
                res = res.append(values, ignore_index=True, sort=False)

    res_describe.to_csv(path_or_buf="df_prapr.csv", index=False)
    utils.lineplot(res, name='prapr_valid_others', x='probability', y='valid', y_label='Number of valid patches', hue='project',
                    x_label='Nominal Flake Rate')
    # utils.lineplot(res, 'valid_patches_std', 'probability', 'std', 'Standard Deviation n', 'project',
    #                 x_label='Nominal Flake Rate')


if __name__ == "__main__":
    main_prapr()
