import csv

from data_sourcing.models import Fixture


def run():
    fixture_ids = [
        'd736eab8', '81ac72d8', 'b800c4ba',
        'bf7873f2', 'd260be24', '5ce80a04',
        '26ff83e6', '4ed4a295', '5290c2da', 'c9b4c96a'
    ]
    # fixtures = [Fixture.objects.get(id=fixture_id) for fixture_id in fixture_ids]
    fixtures = Fixture.objects.all()
    with open('fixtures.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'id', 'competition', 'season', 'date', 'time',
            'home', 'away', 'goals_home', 'goals_away',
            'xG_home', 'xG_away'
        ])
        for fixture in fixtures:
            writer.writerow([
                fixture.id, fixture.competition, fixture.season,
                fixture.date, fixture.time, fixture.home.id,
                fixture.away.id, fixture.goals_home, fixture.goals_away,
                fixture.xG_home, fixture.xG_away
            ])