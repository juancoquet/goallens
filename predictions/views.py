from django.shortcuts import render # type: ignore

from data_sourcing.models import Fixture
from predictions.models import Prediction


def prediction_detail_view(request, fixture_id):
    fixture = Fixture.objects.get(id=fixture_id)
    dd, mm, yyyy = fixture.date.day, fixture.date.month, fixture.date.year
    prediction = Prediction.objects.get(fixture=fixture)
    home_win_prob = int(round(prediction.home_win_prob, 2) * 100)
    away_win_prob = int(round(prediction.away_win_prob, 2) * 100)
    draw_prob = int(round(prediction.draw_prob, 2) * 100)
    while home_win_prob + away_win_prob + draw_prob > 100: # 101%
        draw_prob -= 1
    while home_win_prob + away_win_prob + draw_prob < 100: # 99%
        draw_prob += 1

    return render(request, 'prediction_detail.html', {
        'fixture': fixture,
        'prediction': prediction,
        'dd': str(dd).zfill(2),
        'mm': str(mm).zfill(2),
        'yyyy': yyyy,
        'home_win_prob': home_win_prob,
        'away_win_prob': away_win_prob,
        'draw_prob': draw_prob,
        })