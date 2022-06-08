from django.shortcuts import render # type: ignore

from data_sourcing.models import Fixture
from predictions.models import Prediction


def prediction_detail_view(request, fixture_id):
    fixture = Fixture.objects.get(id=fixture_id)
    dd, mm, yyyy = fixture.date.day, fixture.date.month, fixture.date.year
    prediction = Prediction.objects.get(fixture=fixture)
    return render(request, 'prediction_detail.html', {
        'fixture': fixture,
        'prediction': prediction,
        'dd': str(dd).zfill(2),
        'mm': str(mm).zfill(2),
        'yyyy': yyyy,
        })