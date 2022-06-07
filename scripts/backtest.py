from analysis.back_testing.back_testing import BackTester
from supported_comps import PREDICTION_COMPS


seasons = ['2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
competitions = [k for k in PREDICTION_COMPS.keys()]


xGs_past_games_list = [5, 10]

suppression_range_list = [0.5, 0.75, 1.0, 1.25, 1.5]
conversion_range_list = [0.5, 0.75, 1.0, 1.25, 1.5]
sup_conv_past_games_list = [5, 7, 10]

h_a_weight_list = [0.5, 0.75, 1.0]
h_a_past_games_list = [10]


bt = BackTester(
    seasons=seasons,
    competitions=competitions,
    xGs_past_games_list=xGs_past_games_list,
    suppression_range_list=suppression_range_list,
    conversion_range_list=conversion_range_list,
    sup_conv_past_games_list=sup_conv_past_games_list,
    h_a_weight_list=h_a_weight_list,
    h_a_past_games_list=h_a_past_games_list
)

bt.back_test_params()
bt.save_results()