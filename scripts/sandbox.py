from data_sourcing.models import Fixture
from predictions.predictor import Predictor


fixture = Fixture.objects.get(id='ffb4946c')

predictor = Predictor()
prediction_dict = predictor.generate_prediction(fixture)

for k, v in prediction_dict.items():
    print(f'{k}: {v}')