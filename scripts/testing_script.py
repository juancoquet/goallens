from data_sourcing.models import Fixture, Team
from predictions.predictor import Predictor


predictor = Predictor()
fixture = Fixture.objects.get(id='871109e6')
# TODO: figure out why this prediction forecasts 0xG for the home team man city

def run():
    print(fixture)
    prediction = predictor.generate_prediction(fixture=fixture)

    for k, v in prediction.items():
        if k == 'fixture':
            continue
        print(k, v)



# mci base xG = 2.88
# av suppression = 0.86
# mci conversion = 1.17
# mci performance = 1.25
