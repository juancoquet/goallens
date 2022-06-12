from django.test import TestCase # type: ignore
import pandas as pd

from ..analyst import Analyst
from ..back_testing.back_testing import BackTester


class TestBacktester(TestCase):

    def test_creates_param_combinations_on_init(self):
        bt = BackTester(
            seasons=['2020-2021'],
            competitions=['Premier League'],
            xGs_past_games_list=['a', 'b', 'c'],
            suppression_range_list=[0.2, 0.3],
            conversion_range_list=[0.2, 0.3],
            sup_conv_past_games_list=[3, 4],
            h_a_weight_list=[0.5, 0.6],
            h_a_past_games_list=[3, 4]
        )
        self.assertEqual(len(bt.combinations), 96)
        self.assertEqual(len(bt.combinations[0]), 6)

    def test_save_results(self):
        bt = BackTester(
            seasons=['2020-2021'],
            competitions=['Premier League'],
            xGs_past_games_list=['a', 'b', 'c'],
            suppression_range_list=[0.2, 0.3],
            conversion_range_list=[0.2, 0.3],
            sup_conv_past_games_list=[3, 4],
            h_a_weight_list=[0.5, 0.6],
            h_a_past_games_list=[3, 4]
        )
        data = {
            'probability': [0.0001, 0.024, 0.12, 0.31, 0.324],
            'outcome': [0, 0, 1, 0, 1]
        }
        analyst = Analyst()
        df = pd.DataFrame(data)
        analyst.df_prob_outcomes = df
        analyst.calculate_strikerates()
        analyst.mean_squared_error()
        bt.results = {
            (3, 0.2, 0.2, 3, 0.5, 5): analyst
        }
        # uncomment below line and check that files are saved to disk at:
            # analysis/back_testing/results/001/. should have _params.txt, plot.png and
            # analyst.pickle
        # bt.save_results() # uncomment