from data_sourcing.models import Fixture, Team
from predictions.predictor import Predictor


predictor = Predictor()
fixture = Fixture.objects.get(id='7b4b63d0')
# TODO: figure out why this prediction forecasts 0xG for the home team man city

def run():
    print(fixture)
    predictor._calculate_chance_suppression_scores(fixture)
    print('suppression:', predictor._calculate_chance_suppression_scores(fixture))
    print('conversion:', predictor._calculate_chance_conversion_scores(fixture))
    prediction = predictor.generate_prediction(fixture=fixture)

    for k, v in prediction.items():
        if k == 'fixture':
            continue
        print(k, v)



# mci base xG = 2.88
# av suppression = 0.86
# mci conversion = 1.17
# mci performance = 1.25
