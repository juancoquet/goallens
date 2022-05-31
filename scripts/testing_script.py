from data_sourcing.models import Fixture, Team
from predictions.predictor import Predictor


predictor = Predictor()
fixture = Fixture.objects.get(id='79b8fb6e')
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



# for mcty liv game 37e2fe92 range = 1 (0.5 to 1.5)
# home ga4 xga 4.0
# ga/floor(xga) = 1.0
# inverse = 1 - 1.0 = 0.0
# suppression = 1 - 0.0 * (0.5*1) = 1.0

# away ga0 xga 3.6
# ga/floor(xga) = 0.0
# inverse = 1 - 0.0 = 1.0
# suppression = 1 - 1.0 * (0.5*1) = 0.5


# for leeds av game 79b8fb6e range = 1 (0.5 to 1.5)
# home ga 18 xga 12.6
# ga/floor(xga) = 1.5
# percentage = 1 / 1.5 = 0.6667
# inverse = 1 - 0.6667 = 0.3333
# suppression = 1 + 0.3333 * (0.5*1) = 1.1667 = 1.17

# away ga 5 xga 4.8
# ga/floor(xga) = 1.25
# percentage = 1 / 1.25 = 0.8
# inverse = 1 - 0.8 = 0.2
# suppression = 1 + 0.2 * (0.5*1) = 1.1


# for leeds av game 79b8fb6e range = 0.5 (0.75 to 1.25)
# home ga 18 xga 12.6
# ga/floor(xga) = 1.5
# percentage = 1 / 1.5 = 0.6667
# inverse = 1 - 0.6667 = 0.3333
# suppression = 1 + 0.3333 * (0.5*0.5) = 1.0833 = 1.08

# away ga 5 xga 4.8
# ga/floor(xga) = 1.25
# percentage = 1 / 1.25 = 0.8
# inverse = 1 - 0.8 = 0.2
# suppression = 1 + 0.2 * (0.5*0.5) = 1.05