from analysis.analyst import Analyst

from supported_comps import PREDICTION_LEAGUES


analyst = Analyst()

seasons = ['2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
competitions = [key for key in PREDICTION_LEAGUES.keys()]

df = analyst.create_analysis_df(seasons, competitions)
strikerates = analyst.calculate_strikerates(df)
mse = analyst.weighted_mean_squared_error(strikerates, df)
analyst.pickle_data()