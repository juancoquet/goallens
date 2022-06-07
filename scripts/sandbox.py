# go through each folder
# import the analyst object
# plot the results

import os
import pickle
from analysis.plotting.plotting import plot


for i in range(72):
    dir_name = str(i+1).zfill(3)
    with open(f'analysis/back_testing/results/{dir_name}/analyst.pickle', 'rb') as f:
        analyst = pickle.load(f)
    df = analyst.df
    sr = analyst.strikerates
    mse = analyst.mse
    plot(strikerates=sr, mse=mse, df=df, filename=f'analysis/back_testing/results/{dir_name}/plot')
