from analysis.plotting.plotting import plot
import pickle


for dir_name in range(100):
    dir_name = str(dir_name+1).zfill(3)
    with open(f'analysis/back_testing/storage/params_3/{dir_name}/analyst.pickle', 'rb') as f:
        analyst = pickle.load(f)
    
    with open(f'analysis/back_testing/storage/params_3/{dir_name}/_params.txt', 'r') as f:
        xGs_past_games = f.readline().strip().replace('xGs_past_games: ', '')
        suppression_range = f.readline().strip().replace('suppression_range: ', '')
        conversion_range = f.readline().strip().replace('conversion_range: ', '')
        sup_con_past_games = f.readline().strip().replace('sup_con_past_games: ', '')
        h_a_weight = f.readline().strip().replace('h_a_weight: ', '')
        h_a_past_games = f.readline().strip().replace('h_a_past_games: ', '')
        params = (xGs_past_games, suppression_range, conversion_range, sup_con_past_games, h_a_weight, h_a_past_games)

    sr = analyst.calculate_strikerates()
    df = analyst.df
    mse = analyst.mean_squared_error()
    write_path = f'analysis/back_testing/storage/params_3/{dir_name}/plot'

    plot(sr, mse, df, filename=write_path, params=params)