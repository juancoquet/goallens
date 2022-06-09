from data_sourcing.models import Fixture
from predictions.predictor import Predictor
from predictions.models import Prediction


predictor = Predictor()
fixture = Fixture.objects.get(id='ffb4946c')
prediction = predictor.generate_prediction(fixture)


def run():
    Prediction.objects.create(
        fixture=fixture,
        forecast_hxG=prediction['forecast_xGs']['home'],
        forecast_axG=prediction['forecast_xGs']['away'],
        prob_hg_0=prediction['prob_0_goals']['home'],
        prob_hg_1=prediction['prob_1_goals']['home'],
        prob_hg_2=prediction['prob_2_goals']['home'],
        prob_hg_3=prediction['prob_3_goals']['home'],
        prob_hg_4=prediction['prob_4_goals']['home'],
        prob_hg_5=prediction['prob_5_goals']['home'],
        prob_hg_6=prediction['prob_6_goals']['home'],
        prob_hg_7=prediction['prob_7_goals']['home'],
        prob_ag_0=prediction['prob_0_goals']['away'],
        prob_ag_1=prediction['prob_1_goals']['away'],
        prob_ag_2=prediction['prob_2_goals']['away'],
        prob_ag_3=prediction['prob_3_goals']['away'],
        prob_ag_4=prediction['prob_4_goals']['away'],
        prob_ag_5=prediction['prob_5_goals']['away'],
        prob_ag_6=prediction['prob_6_goals']['away'],
        prob_ag_7=prediction['prob_7_goals']['away'],
        likely_hg=prediction['likely_scoreline']['home'],
        likely_ag=prediction['likely_scoreline']['away'],
    )