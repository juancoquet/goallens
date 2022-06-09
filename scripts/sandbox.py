from data_sourcing.models import Fixture
from predictions.predictor import Predictor


predictor = Predictor()
fixture = Fixture.objects.get(id='ffb4946c')
prediction = predictor.generate_prediction(fixture)
for k, v in prediction.items():
    print(k, v)