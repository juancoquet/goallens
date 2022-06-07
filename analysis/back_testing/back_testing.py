from copyreg import pickle
import datetime as dt
import itertools
import os
import pickle

from ..analyst import Analyst
from ..plotting.plotting import plot


class BackTester:

    def __init__(self, seasons: list[str], competitions: list[str],
                xGs_past_games_list, suppression_range_list,
                 conversion_range_list, sup_conv_past_games_list,
                 h_a_weight_list, h_a_past_games_list):
        self.seasons = seasons
        self.competitions = competitions
        self.xGs_past_games_list = xGs_past_games_list
        self.suppression_range_list = suppression_range_list
        self.conversion_range_list = conversion_range_list
        self.sup_conv_past_games_list = sup_conv_past_games_list
        self.h_a_weight_list = h_a_weight_list
        self.h_a_past_games_list = h_a_past_games_list
        self.combinations = list(itertools.product(
            xGs_past_games_list, suppression_range_list,
            conversion_range_list, sup_conv_past_games_list,
            h_a_weight_list, h_a_past_games_list
        ))
        self.results = {}
        self.best_results = []
        self.last_runtime = None

    def back_test_params(self):
        for i, params in enumerate(self.combinations):
            print(f'back testing params {i+1} of {len(self.combinations)}')
            if self.last_runtime is not None:
                print(f'estimated time remaining: {(len(self.combinations) - i) * self.last_runtime}')
            start_time = dt.datetime.now()

            xGs_past_games_list = params[0]
            suppression_range_list = params[1]
            conversion_range_list = params[2]
            sup_conv_past_games_list = params[3]
            h_a_weight_list = params[4]
            h_a_past_games_list = params[5]
            analyst = Analyst()
            analyst.create_analysis_df(
                self.seasons, self.competitions,
                xGs_past_games_list, suppression_range_list,
                conversion_range_list, sup_conv_past_games_list,
                h_a_weight_list, h_a_past_games_list
            )
            analyst.calculate_strikerates()
            analyst.mean_squared_error()
            
            self.results[params] = analyst
            worst_performance = params
            if len(self.results) > 100:
                for key, _analyst in self.results.items():
                    if _analyst.mse > self.results[worst_performance].mse:
                        worst_performance = key
                del self.results[worst_performance]

            end_time = dt.datetime.now()
            self.last_runtime = end_time - start_time
            for _ in range(5):
                print('~' * 80, '\n')
        
        self.results = {k: v for k, v in sorted(self.results.items(), key=lambda item: item[1].mse)}

    def save_results(self):
        for i, (params, analyst) in enumerate(self.results.items()):
            i = str(i+1).zfill(3)
            directory = os.path.join(os.getcwd(), 'analysis', 'back_testing', 'results', i)
            os.makedirs(directory, exist_ok=True)
            with open(os.path.join(directory, '_params.txt'), 'w') as f:
                f.write(f'xGs_past_games: {params[0]}\n')
                f.write(f'suppression_range: {params[1]}\n')
                f.write(f'conversion_range: {params[2]}\n')
                f.write(f'sup_conv_past_games: {params[3]}\n')
                f.write(f'h_a_weight: {params[4]}\n')
                f.write(f'h_a_past_games: {params[5]}\n')
            sr = analyst.strikerates
            mse = analyst.mse
            df = analyst.df
            plot_path = os.path.join(directory, 'plot')
            plot(sr, mse, df, title=None, filename=plot_path)
            # pickle analylst
            with open(os.path.join(directory, 'analyst.pickle'), 'wb') as f:
                pickle.dump(analyst, f)