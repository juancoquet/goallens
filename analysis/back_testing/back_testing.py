import concurrent.futures
import datetime as dt
from django import db # type: ignore
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
        self.num_combinations = len(self.combinations)
        self.results = {}
        self.best_results = []
        self.start_time = None

    def _back_test_param_set(self, params):
            print(f'backtesting params: {params}')
            for _ in range(5):
                print('#' * 80)
            db.connections.close_all()
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

            curr_index = self.combinations.index(params) + 1
            remaining = self.num_combinations - curr_index
            elapsed_time = dt.datetime.now() - self.start_time
            remaining_time = elapsed_time * remaining / curr_index
            print('-' * 140)
            print('-' * 140)
            print(f'completed {curr_index}/{self.num_combinations}')
            print(f'{elapsed_time} elapsed')
            print(f'estimated time remaining: {remaining_time}')
            print('-' * 140)
            print('-' * 140)

            return (params, analyst)

    def back_test_params(self):
        self.start_time = dt.datetime.now()

        # multiprocessing loop
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(self._back_test_param_set, self.combinations)
        results = sorted(results, key=lambda x: x[1].mse)[:100]

        self.results = {params: analyst for params, analyst in results}

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
            plot(sr, mse, df, title=None, filename=plot_path, params=params)
            # pickle analylst
            with open(os.path.join(directory, 'analyst.pickle'), 'wb') as f:
                pickle.dump(analyst, f)