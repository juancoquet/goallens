from data_sourcing.models import Fixture, Team
from predictions.predictor import Predictor


predictor = Predictor()
fixture = Fixture.objects.get(id='7b4b63d0')
# TODO: figure out why this prediction forecasts 0xG for the home team man city

def run():
    print(fixture)
    predictor._calculate_chance_suppression_scores(fixture)
    print('base xG', predictor._calculate_base_forecast_xGs(fixture))
    print('base xGA', predictor._calculate_base_forecast_xGAs(fixture))
    print('suppression:', predictor._calculate_chance_suppression_scores(fixture))
    print('conversion:', predictor._calculate_chance_conversion_scores(fixture))
    print('home performance:', predictor._calculate_home_away_performance(fixture, 'home'))
    print('away performance:', predictor._calculate_home_away_performance(fixture, 'away'))
    prediction = predictor.generate_prediction(fixture=fixture)

    for k, v in prediction.items():
        if k == 'fixture':
            continue
        print(k, v)



# fxG = ((bfxG * conversion) + (o_bfxGA * o_suppression)) / 2 * h_a_performance

# %%
home_fxG = (((2.88 * 1.17) + (1.42 * 0.86)) / 2) * 1.25 
away_fxG = (((1.48 * 1.06) + (0.88 * 1.0)) / 2) * 1.0 
home_fxG, away_fxG