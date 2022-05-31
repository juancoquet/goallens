from data_sourcing.models import Fixture, Team
from predictions.predictor import Predictor


predictor = Predictor()
fixture = Fixture.objects.get(id='7b4b63d0')
# TODO: figure out why this prediction forecasts 0xG for the home team man city

def run():
    print(fixture)
    # predictor._calculate_chance_suppression_scores(fixture)
    # print('suppression:', predictor._calculate_chance_suppression_scores(fixture)) # problem is here
    prediction = predictor.generate_prediction(fixture=fixture)

    for k, v in prediction.items():
        if k == 'fixture':
            continue
        print(k, v)




# for bri 0-2 tot 59b3ee40 range=1
# home g=1, xg=3.8
# base_conv = 0.3333
# inverse = 0.6667
# home_conversion = 0.6667

# away g=14, xg=9.3
# base conv = 1.5556
# percentage = 0.6429
# inverse = 0.3571
# away_conversion = 1.1786