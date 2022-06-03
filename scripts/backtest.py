from analysis.back_testing.back_testing import BackTester
from supported_comps import PREDICTION_COMPS


seasons = ['2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
# seasons = ['2020-2021']
competitions = [k for k in PREDICTION_COMPS.keys()]


xGs_past_games_list = [3, 5, 10]

suppression_range_list = [0.2, 1.0, 1.6]
conversion_range_list = [0.2, 1.0, 1.6]
sup_conv_past_games_list = [3, 5, 10]

h_a_weight_list = [0.5, 1.0, 1.5]
h_a_past_games_list = [5, 10, 15]


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