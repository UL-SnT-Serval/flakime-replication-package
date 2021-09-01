import utils
import time
import pandas
import os

def draw_distribution(folder):    
    for file_path, file_name in utils.list_files(folder):
        data = pandas.read_csv(file_path, sep=';').set_index('name')
        title = os.path.splitext(file_name)[0]

        print('--------------------------------------------------')
        print('Project: ' + title)
        print('--------------------------------------------------')
        total = data.shape[0]
        total_not_null = data.loc[data['probability'] > 0.].shape[0]
        median = data['probability'].median()
        print('median: ' + str(median))
        print('total: ' + str(total))
        print('percentage flaking: ' + str(float(total_not_null) / float(total) * 100))

        utils.distribution(data, 'probability-distribution-' + title, 'probability', binwidth=0.05, x_label='Probability', y_label='Number of Tests')

if __name__ == "__main__":
    t_start = time.perf_counter()
    draw_distribution('data/overview')
    t_stop = time.perf_counter()

    print('\n')
    print("--------------------------------------------------")
    print('Elapsed time:{:.1f} [sec]'.format(t_stop-t_start))
    print("--------------------------------------------------") 