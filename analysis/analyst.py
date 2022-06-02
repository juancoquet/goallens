from cmath import nan
from datetime import date
from decimal import Decimal
import math
from matplotlib import pyplot as plt # type: ignore
import pandas as pd # type: ignore
import pickle
import re

from data_sourcing.models import Fixture
from predictions.predictor import NotEnoughDataError, Predictor
from supported_comps import PREDICTION_LEAGUES


class Analyst:

    def __init__(self):
        self.df = None
        self.strikerates = None
        self.mse = None

    def create_analysis_df(self, seasons: list[str], competitions: list[str]):
        """creates a dataframe where each row is a prediction probability and its respective outcome,
        for all predictions in given seasons and competitions.
        
        Args:
            seasons (list[str]): the seasons to analyse, formatted ['YYYY-YYYY']
            competitions (list[str]): the competitions to analyse
        """
        if type(seasons) != list:
            raise TypeError('seasons must be a list of strings with format ["yyyy-yyyy"]')
        if type(competitions) != list:
            raise TypeError('competitions must be a list of strings')
        for season in seasons:
            self._validate_season(season)
        for competition in competitions:
            self._validate_competition(competition)

        predictor = Predictor()
        data = {'probability': [], 'outcome': []}
        
        for season in seasons:
            for competition in competitions:
                fixtures = Fixture.objects.filter(competition=competition, season=season)
                for fixture in fixtures:
                    print(f'processing {fixture.id}, {len(data["probability"])} records so far')
                    try:
                        prediction = predictor.generate_prediction(fixture)
                    except NotEnoughDataError:
                        continue
                    pred_copy = prediction.copy()
                    outcomes = self._check_prediction_outcomes(prediction)
                    combined = self._combine_predictions_and_outcomes(pred_copy, outcomes)
                    for prob, outcome in combined:
                        data['probability'].append(prob)
                        data['outcome'].append(outcome)
                    
        df = pd.DataFrame(data)
        print(f'{len(df)} predictions analysed')
        self.df = df
        return df

    def calculate_strikerates(self, df: pd.DataFrame):
        """calculates the strikerates for probability ranges of 2.5%. If there are no predictions within
        a particular range, the mean prediction value and stirke rate for the range are set to None.
        Args:
            df (pd.DataFrame): the dataframe to analyse, which should have been created by Analyst.create_analysis_df().
        Returns:
            dict: a dict of the form {percent_range: {'mean_prediction': mean(probs_within_range), 'strikerate': strikerate}, ...}
        """
        strikerates = {}
        lower_bound = 0.0
        while lower_bound < 100:
            upper_bound = lower_bound + 2.5
            l_bound = lower_bound / 100
            u_bound = upper_bound / 100
            preds_within_range = df[(df['probability'] >= l_bound) & (df['probability'] < u_bound)]
            mean_prediction = preds_within_range['probability'].mean()
            if math.isnan(mean_prediction):
                mean_prediction = None
            try:
                strikerate = len(preds_within_range[preds_within_range['outcome'] == 1]) / len(preds_within_range)
            except ZeroDivisionError:
                strikerate = None
            strikerates[f'{lower_bound}-{upper_bound}'] = {'mean_prediction': mean_prediction, 'strikerate': strikerate}
            lower_bound += 2.5
        self.strikerates = strikerates
        return strikerates


    
    
    def mean_squared_error(self, strikerates: dict):
        """calculates the mean squared error for the given strikerates.
        Args:
            strikerates (dict): the strikerates to calculate the MSE for. should be a dict output
            by Analyst.calculate_strikerates().
        Returns:
            float: the mean squared error
        """
        mse = 0
        count = 0
        for preds_and_strikerates in strikerates.values():
            observed = preds_and_strikerates['strikerate']
            predicted = preds_and_strikerates['mean_prediction']
            if observed is None or predicted is None:
                continue
            mse += (observed - predicted) ** 2
            count += 1
        mse /= count
        mse = round(mse, 4)
        self.mse = mse
        return mse

    def pickle_data(self):
        """pickle the dataframe, mse, and strikerates.
        """
        with open('analysis/data/data.pickle', 'wb') as f:
            pickle.dump(self.df, f)
        with open('analysis/data/mse.pickle', 'wb') as f:
            pickle.dump(self.mse, f)
        with open('analysis/data/strikerates.pickle', 'wb') as f:
            pickle.dump(self.strikerates, f)

    def _check_prediction_outcomes(self, prediction: dict):
        """check the outcomes of a prediction.
        reads the probabilities forecasted for each number of goals for home and away teams,
        and compares them to the actual result of the fixture.
                
        Args:
            prediction (dict): the prediction to check. Note that this isn't a predictions.models.Prediction
            object, its the dict returned by the Predictor.generate_prediction method.
        Returns:
            dict: a dict of the form {'0_goals': {'home': 0, 'away': 0}, ...} where the keys are the number of
            goals and the values are a dictionary that maps 'home' and 'away' to 0 or 1 depending on whether
            the prediction was correct or not.
        """
        fixture = prediction['fixture']
        del prediction['fixture']
        del prediction['forecast_xGs']
        del prediction['likely_scoreline']

        outcomes = {}
        for goals, _ in enumerate(prediction.keys()):
            this_outcome = {'home': 0, 'away': 0}
            if goals == fixture.goals_home:
                this_outcome['home'] = 1
            if goals == fixture.goals_away:
                this_outcome['away'] = 1
            outcomes[f'{goals}_goals'] = this_outcome
        
        return outcomes

    def _combine_predictions_and_outcomes(self, prediction: dict, outcomes: dict):
        """combines forecast probabilities for a prediction's goal events with their 
        respective outcome.
        
        Args:
            prediction (dict): the prediction to check. Note that this isn't a predictions.models.Prediction
            object, its the dict returned by the Predictor.generate_prediction method.
            outcomes (dict): the outcomes of the predictions, as generated by Analyst.check_prediction_outcomes().
        Returns:
            list[tuple]: a list of tuples of the form (probability, outcome)
        """
        del prediction['fixture']
        del prediction['forecast_xGs']
        del prediction['likely_scoreline']

        combined = []
        for probs, outcome in zip(prediction.values(), outcomes.values()):
            home_prob = probs['home']
            home_outcome = outcome['home']
            away_prob = probs['away']
            away_outcome = outcome['away']
            combined.append((home_prob, home_outcome))
            combined.append((away_prob, away_outcome))

        return combined

    def _validate_competition(self, competition):
        if competition not in PREDICTION_LEAGUES:
            valid_comps = [k for k in PREDICTION_LEAGUES.keys()]
            raise ValueError(f'competion must be one of {valid_comps} – {competition} is invalid')

    def _validate_season(self, season):
        season_re = r'\d{4}-\d{4}'
        if not re.match(season_re, season):
            raise ValueError(f'season must be in format yyyy-yyyy – {season} is invalid')
        else:
            start_yr = int(season[:4])
            end_yr = int(season[-4:])
            if end_yr - start_yr != 1:
                raise ValueError(f'season must be a one year period, e.g. 2019-2020 – {season} is invalid')
            if start_yr < 2010 or end_yr > date.today().year:
                raise ValueError(f'season must be between 2010 and {date.today().year} – {season} is invalid')