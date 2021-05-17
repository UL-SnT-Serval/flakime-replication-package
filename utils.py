import matplotlib
matplotlib.use('Agg')

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import re

from matplotlib import colors

CACHE = '{}_cache.csv'
HDF5_CACHE = '{}_cache.h5'

FIGURE_FOLDER = 'figures/'
EXTENSION = '.pdf'


def list_dirs(path):
    return [(os.path.join(os.path.join(path,dI)), dI) for dI in os.listdir(path) if os.path.isdir(os.path.join(path,dI))]


def find_dirs(path, regex):
    return [f for f in list_dirs(path) if re.match(regex, f[1])]


def list_files(path):
    return [(os.path.join(os.path.join(path,dI)), dI) for dI in os.listdir(path) if os.path.isfile(os.path.join(path,dI))]


def find_files(path, regex):
    return [f[0] for f in list_files(path) if re.match(regex, f[1])]


def get_folder(path, project, bug_id, flake_rate, strategy):
    return os.path.normpath(re.sub(r'\\$|/$', '', path) + '/' + project + '/' + bug_id + '/' + flake_rate + '/' + strategy)

def walk_folders(path):
    for project_dir, project in list_dirs(path):
        for bug_id_dir, bug_id in list_dirs(project_dir):
            for flake_rate_dir, flake_rate in list_dirs(bug_id_dir):
                for strategy_dir, strategy in list_dirs(flake_rate_dir):
                    yield [strategy_dir, project, bug_id, flake_rate, strategy]


def color_palette(data, hue):
    n_colors = len(data[hue].unique())
    return sns.color_palette("cubehelix", n_colors=n_colors)


def lineplot(data, name, x, y, hue=None, y_label='', x_label='', x_lim=None, y_lim=None, fig_size=(6,4), legend_pos='best', style=None):
    fig = plt.figure(figsize=fig_size)
    sns.set(style="white", color_codes=True, font_scale=1.5)

    palette = color_palette(data, hue)

    g = sns.lineplot(x=x, y=y, hue=hue, data=data, palette=palette, legend="full", style=style)

    fig.tight_layout()

    if not legend_pos:
        g.legend_.remove()
    else:
        plt.legend(loc=legend_pos, prop={'size': 15})

    plt.ylabel(y_label, fontsize=15)
    plt.xlabel(x_label, fontsize=15)

    if y_lim != None and len(y_lim) == 2:
        plt.ylim(y_lim)

    if x_lim != None and len(x_lim) == 2:
        plt.xlim(x_lim)

    plt.savefig(FIGURE_FOLDER + name + EXTENSION, dpi=300, bbox_inches='tight')
    plt.close('all')


def boxplot(data, name, x, y, hue=None, y_label='', x_label='', x_lim=None, y_lim=None, fig_size=(6,4), legend_pos='best', log_scale=False, sparse_tick=False):
    fig = plt.figure(figsize=fig_size)
    sns.set(style="ticks", color_codes=True, font_scale=1.5)

    palette = color_palette(data, hue)

    if data[x].dtype == np.float64:
        data[x] = data[x].apply('{:,.2f}'.format)

    g = sns.boxplot(x=x, y=y, hue=hue, data=data, palette=palette, linewidth=1)
    sns.despine(offset=10, trim=False)

    plt.tick_params(axis='both', which='both', labelsize=15)

    plt.ylabel(y_label, fontsize=15)
    plt.xlabel(x_label, fontsize=15)

    if hue is not None:
        if not legend_pos:
            g.legend_.remove()
        else:
            handles, labels = g.get_legend_handles_labels()
            plt.legend(loc=legend_pos, prop={'size': 15}, handles=handles[0:], labels=labels[0:])

    if y_lim != None and len(y_lim) == 2:
        plt.ylim(y_lim)

    if x_lim != None and len(x_lim) == 2:
        plt.xlim(x_lim)

    if log_scale:    
        g.set_yscale('log')

    if sparse_tick:
        for label in g.xaxis.get_ticklabels()[1::2]:
            label.set_visible(False)
    else:
        plt.xticks(rotation=45)

    fig.tight_layout()

    plt.savefig(FIGURE_FOLDER + name + EXTENSION, dpi=300, bbox_inches='tight')
    plt.close('all')