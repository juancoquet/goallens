import math
import numpy as np # type: ignore
from scipy.stats import poisson # type: ignore

from data_sourcing.models import Fixture
from predictions.predictor import Predictor


fixture_id = '7b4b63d0'
predictor = Predictor()

def run():
    fixture = Fixture.objects.get(id=fixture_id)
    home_past_5 = predictor._get_home_team_past_n_fixtures(fixture, n=5)
    away_past_5 = predictor._get_away_team_past_n_fixtures(fixture, n=5)
    # home
    home_past_5_GAs = []
    home_past_5_xGAs = []
    for f in home_past_5:
        if f.away == fixture.home:  # if was away in the fixture, append home team's xG
            if f.xG_home is not None:
                home_past_5_GAs.append(f.goals_home)
                home_past_5_xGAs.append(float(f.xG_home))
            else:
                home_past_5_GAs.append(f.goals_home)
                home_past_5_xGAs.append(f.goals_home)
        else:
            if f.xG_away is not None:
                home_past_5_GAs.append(f.goals_away)
                home_past_5_xGAs.append(float(f.xG_away))
            else:
                home_past_5_GAs.append(f.goals_away)
                home_past_5_xGAs.append(f.goals_away)
    total_GA = sum(home_past_5_GAs)
    total_xGA = sum(home_past_5_xGAs)
    most_likely_GA = math.floor(total_xGA)
    unweighted_home_def_score = total_GA / most_likely_GA # dumb home defence score, something like 0.9 for a positive score, 1.1 for a negative score
    weighting_delta = 1 - unweighted_home_def_score # 0.1 postivie, -0.1 negative
    w = 1
    weighted_delta = w * weighting_delta # if w=0.5, 0.05 positive, -0.05 negative
    weighted_home_def_score = 1 - weighted_delta # 0.95 positive, 1.05 negative
    print('home:')
    print(f'GA: {total_GA}, xGA: {total_xGA} | w={w}')
    print(f'weighted_home_def_score: {weighted_home_def_score}')
    # away
    away_past_5_GAs = []
    away_past_5_xGAs = []
    for f in away_past_5:
        if f.away == fixture.away:  # if was away in the fixture, append home team's xG
            if f.xG_home is not None:
                away_past_5_GAs.append(f.goals_home)
                away_past_5_xGAs.append(float(f.xG_home))
            else:
                away_past_5_GAs.append(f.goals_home)
                away_past_5_xGAs.append(f.goals_home)
        else:
            if f.xG_away is not None:
                away_past_5_GAs.append(f.goals_away)
                away_past_5_xGAs.append(float(f.xG_away))
            else:
                away_past_5_GAs.append(f.goals_away)
                away_past_5_xGAs.append(f.goals_away)
    total_GA = sum(away_past_5_GAs)
    total_xGA = sum(away_past_5_xGAs)
    most_likely_GA = math.floor(total_xGA)
    unweighted_away_def_score = total_GA / most_likely_GA # dumb home defence score, something like 0.9 for a positive score, 1.1 for a negative score
    weighting_delta = 1 - unweighted_away_def_score # 0.1 postivie, -0.1 negative
    w = 1
    weighted_delta = w * weighting_delta # if w=0.5, 0.05 positive, -0.05 negative
    weighted_away_def_score = 1 - weighted_delta # 0.95 positive, 1.05 negative
    print('away:')
    print(f'GA: {total_GA}, xGA: {total_xGA} | w={w}')
    print(f'weighted_away_def_score: {weighted_away_def_score}')
