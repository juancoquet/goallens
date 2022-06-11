import datetime
from django.core.paginator import Paginator # type: ignore
from django.db.models import Q # type: ignore
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

    context = {
        'fixture': fixture,
        'prediction': prediction,
        'dd': str(dd).zfill(2),
        'mm': str(mm).zfill(2),
        'yyyy': yyyy,
        'home_win_prob': home_win_prob,
        'away_win_prob': away_win_prob,
        'draw_prob': draw_prob,
    }
    for g in range(8):
        prob_hg = getattr(prediction, f'prob_hg_{g}')
        prob_ag = getattr(prediction, f'prob_ag_{g}')
        context[f'prob_hg_{g}'] = float(prob_hg * 100)
        context[f'prob_ag_{g}'] = float(prob_ag * 100)

    prev_pred_home = Prediction.objects.filter(
        Q(fixture__date__lt=fixture.date) &
        (Q(fixture__home=prediction.fixture.home) | Q(fixture__away=prediction.fixture.home))
        ).order_by('-fixture__date').first()
    
    prev_pred_away = Prediction.objects.filter(
        Q(fixture__date__lt=fixture.date) &
        (Q(fixture__home=prediction.fixture.away) | Q(fixture__away=prediction.fixture.away))
        ).order_by('-fixture__date').first()

    next_pred_home = Prediction.objects.filter(
        Q(fixture__date__gt=fixture.date) &
        (Q(fixture__home=prediction.fixture.home) | Q(fixture__away=prediction.fixture.home))
        ).order_by('fixture__date').first()

    next_pred_away = Prediction.objects.filter(
        Q(fixture__date__gt=fixture.date) &
        (Q(fixture__home=prediction.fixture.away) | Q(fixture__away=prediction.fixture.away))
        ).order_by('fixture__date').first()
    
    context['prev_prediction_home'] = prev_pred_home
    context['prev_prediction_away'] = prev_pred_away
    context['next_prediction_home'] = next_pred_home
    context['next_prediction_away'] = next_pred_away

    return render(request, 'prediction_detail.html', context)


def prediction_list_view(request):
    seasons = set(Fixture.objects.values_list('season', flat=True).order_by('season').distinct())
    seasons = sorted(seasons, reverse=True)
    competitions = set(Prediction.objects.values_list('fixture__competition', flat=True).order_by('fixture__competition').distinct())

    season_q = request.GET.get('season')
    competition_q = request.GET.get('competition')
    team_q = request.GET.get('team')
    order_q = request.GET.get('order')
    
    predictions = Prediction.objects.all().order_by('-fixture__date')
    if season_q:
        predictions = predictions.filter(fixture__season=season_q)
    if competition_q:
        predictions = predictions.filter(fixture__competition=competition_q)
    if team_q:
        predictions = predictions.filter(
            Q(fixture__home__name__icontains=team_q) | Q(fixture__away__name__icontains=team_q) |
            Q(fixture__home__short_name__icontains=team_q) | Q(fixture__away__short_name__icontains=team_q)
        )
    if order_q == 'asc':
        predictions = predictions.order_by('fixture__date')
    elif order_q == 'desc':
        predictions = predictions.order_by('-fixture__date')

    predictions = predictions
    paginator = Paginator(predictions, 50)
    page = request.GET.get('page')
    predictions = paginator.get_page(page)

    context = {
        'seasons': seasons,
        'competitions': competitions,
        'predictions': predictions,
        'season_q': season_q,
        'competition_q': competition_q,
        'team_q': team_q,
        'order_q': order_q,
    }
    return render(request, 'prediction_list.html', context)


def prediction_upcoming_view(request):
    today = datetime.date.today()
    # today = datetime.date(2022, 5, 14)
    upcoming_preds = Prediction.objects.filter(fixture__date__gte=today).order_by('fixture__date')
    premier_league = upcoming_preds.filter(fixture__competition='Premier League')
    la_liga = upcoming_preds.filter(fixture__competition='La Liga')
    ligue_1 = upcoming_preds.filter(fixture__competition='Ligue 1')
    bundesliga = upcoming_preds.filter(fixture__competition='Bundesliga')
    serie_a = upcoming_preds.filter(fixture__competition='Serie A')
    preds = {
        'Premier League': premier_league,
        'La Liga': la_liga,
        'Ligue 1': ligue_1,
        'Bundesliga': bundesliga,
        'Serie A': serie_a,
    }
    context = {
        'predictions': preds,
    }
    return render(request, 'prediction_upcoming.html', context)