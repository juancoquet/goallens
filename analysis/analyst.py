import enum


class Analyst:

    def check_prediction_outcomes(self, prediction: dict):
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