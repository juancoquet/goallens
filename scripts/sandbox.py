from analysis.plotting.plotting import plot
import pickle
import os


for i in range(100):
    dir_name = str(i+1).zfill(3)
    with open(f'analysis/back_testing/storage/params_3/{dir_name}/_params.txt', 'r') as f:
        xGs_past_games = f.readline().strip().replace('xGs_past_games: ', '')
        suppression_range = f.readline().strip().replace('suppression_range: ', '')
        conversion_range = f.readline().strip().replace('conversion_range: ', '')
        sup_conv_past_games = f.readline().strip().replace('sup_conv_past_games: ', '')
        h_a_weight = f.readline().strip().replace('h_a_weight: ', '')
        h_a_past_games = f.readline().strip().replace('h_a_past_games: ', '')
    params = (xGs_past_games, suppression_range, conversion_range, sup_conv_past_games, h_a_weight, h_a_past_games)

    # unpickle analyst
    with open(f'analysis/back_testing/storage/params_3/{dir_name}/analyst.pickle', 'rb') as f:
        analyst = pickle.load(f)
    
    df = analyst.df
    strikerates = analyst.strikerates
    mse = analyst.mean_squared_error()
    plot_path = f'analysis/back_testing/storage/params_3/{dir_name}/plot'

    plot(strikerates, mse, df, params=params, filename=plot_path)
