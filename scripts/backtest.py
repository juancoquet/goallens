from analysis.back_testing.back_testing import BackTester
from supported_comps import PREDICTION_COMPS
import os
import time


seasons = ['2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
competitions = [k for k in PREDICTION_COMPS.keys()]


xGs_past_games_list = [5, 10]

suppression_range_list = [0.5, 0.75, 1.0, 1.25, 1.5]
conversion_range_list = [0.5, 0.75, 1.0, 1.25, 1.5]
sup_conv_past_games_list = [5, 7, 10]

h_a_weight_list = [0.5, 0.75, 1.0]
h_a_past_games_list = [10]


# second generation of backtesting
# xGs_past_games_list = [10]

# suppression_range_list = [0.5, 0.7, 0.9, 1.1, 1.3, 1.5]
# conversion_range_list = [0.5, 0.7, 0.9, 1.1, 1.3, 1.5]
# sup_conv_past_games_list = [10]

# h_a_weight_list = [0.5, 0.7, 0.9, 1.1, 1.3, 1.5]
# h_a_past_games_list = [10]


# dummy run
# xGs_past_games_list = [5]
# suppression_range_list = [1.0]
# conversion_range_list = [1.0]
# sup_conv_past_games_list = [5]
# h_a_weight_list = [1.0]
# h_a_past_games_list = [10]



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

for i in range(4):
    i += 1
    bt.combinations = []
    with open(f'scripts/bt_params/params_{i}.txt', 'r') as f:
        for line in f:
            params = line.strip().replace('(', '').replace(')', '').split(',')
            params = [p.strip() for p in params]
            params[0] = int(params[0])
            params[1] = float(params[1])
            params[2] = float(params[2])
            params[3] = int(params[3])
            params[4] = float(params[4])
            params[5] = int(params[5])
            params = tuple(params)
            bt.combinations.append(params)
            bt.num_combinations = len(bt.combinations)

    bt.num_combinations = len(bt.combinations)

    bt.back_test_params()
    bt.save_results()

    os.system(f'cp -r analysis/back_testing/results/ analysis/back_testing/storage/params_{i}/')
    os.system('rm -rf analysis/back_testing/results/*')
    print('copied results to storage')
    # sleep 30 mins
    time.sleep(1800)



# standard xG vs goals scored mse:
# 0.9728408461623658
# this is the mse of observed xG vs observed goals scored