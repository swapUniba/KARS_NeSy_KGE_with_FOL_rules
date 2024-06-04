import scipy.stats as stats
import os
import pandas as pd
import numpy as np


def compute_kt(x, y):

	# group the recommendation lists by user
    grp_x = x.groupby('user')['item'].agg(list).reset_index()
    grp_x.columns = ['user', 'item_x']

    grp_y = y.groupby('user')['item'].agg(list).reset_index()
    grp_y.columns = ['user', 'item_y']

    # merge the top-k for each user
    merged = grp_x.set_index('user').join(grp_y.set_index('user')).reset_index()

    kt_values = []
    p_values = []

    # compute the KT and the p-value of the two top-k lists for each user
    for i, row in merged.iterrows():
        kt, p = stats.kendalltau(row['item_x'], row['item_y'])
        kt_values.append(kt)
        p_values.append(p)

    kt_values = [x for x in kt_values if ~np.isnan(x)]
    p_values = [x for x in p_values if ~np.isnan(x)]
    
    # avg of KT and p-values
    avg_kt = sum(kt_values) / len(kt_values)
    avg_p = sum(p_values) / len(p_values)

    return avg_kt, avg_p


datasets = ['movielens', 'dbbook', 'lastfm']
dims = ['dim256', 'dim512', 'dim768']
tops = ['top5',]

# single file keeping each couple ui-uip+rules and uip-uip + rules
fout = open('kendall_taus_avg.tsv', 'w', encoding='utf-8')

for dataset in datasets:
    fout.write('\n\n\n'+dataset+'\n')
    for top in tops:
        fout.write(top+'\n')
        for dim in dims:
            fout.write('\n\n'+dim+'\n')
            fout.write('truth\tpred\tkt\tp-value\t\ttruth\tpred\tkt\tp-value\n')

            prediction_folder = dataset+'/'+dim+'/'+top+'/'
            preds = os.listdir(prediction_folder)

            ui = pd.read_csv(prediction_folder+'ui.tsv', sep='\t', names=['user', 'item', 'score'])
            uip = pd.read_csv(prediction_folder+'uip.tsv', sep='\t', names=['user', 'item', 'score'])

            for pred in preds:

                current_pred = pd.read_csv(prediction_folder+pred, sep='\t', names=['user', 'item', 'score'])

                ui_tau, ui_p = compute_kt(ui, current_pred)
                uip_tau, uip_p = compute_kt(uip, current_pred)

                fout.write(f'ui\t{pred}\t{ui_tau}\t{ui_p}\t\tuip\t{pred}\t{uip_tau}\t{uip_p}\n')

            print(f'Finished {dataset} {dim} {top}')
            

fout.flush()
fout.close()