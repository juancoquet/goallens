from django.db.utils import IntegrityError # type: ignore
from django.test import TestCase # type: ignore

from data_sourcing import models


class TestTeamModel(TestCase):

    def setUp(self):
        models.Team.objects.create(
            id='19538871',
            name='Manchester United',
            short_name='Manchester Utd',
        )

    def test_create_new_team(self):
        self.assertEqual(len(models.Team.objects.all()), 1)

    def test_id_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            models.Team.objects.create(
                id='19538871',
                name='Liverpool',
                short_name='Liverpool',
            )

    def test_id_required(self):
        with self.assertRaises(IntegrityError):
            models.Team.objects.create(
                id=None,
                name='Liverpool',
                short_name='Liverpool',
            )

    def test_name_required(self):
        with self.assertRaises(IntegrityError):
            models.Team.objects.create(
                id='822bd0ba',
                name=None,
                short_name='Liverpool',
            )

    def test_short_name_required(self):
        with self.assertRaises(IntegrityError):
            models.Team.objects.create(
                id='822bd0ba',
                name='Liverpool',
                short_name=None
            )

    def test_string_representation(self):
        team = models.Team.objects.get(id='19538871')
        self.assertEqual(str(team), 'Manchester United')


class TestFixtureModel(TestCase):

    ### helper methods ###
    
    def _create_fixture(self, id="e62685d4", competition="Premier League",
        season="2021-2022", date="2021-08-14", time="12:30:00", home=True,
        away=True, goals_home=0, goals_away=5, xG_home=1.5, xG_away=3.8,
    ):
        if home is not None:
            home = self.home
        if away is not None:
            away = self.away
        fixture = models.Fixture.objects.create(
            id=id,
            competition=competition,
            season=season,
            date=date,
            time=time,
            home=home,
            away=away,
            goals_home=goals_home,
            goals_away=goals_away,
            xG_home=xG_home,
            xG_away=xG_away,
        )
        return fixture

    ### end helper methods ###

    def setUp(self):
        self.home = models.Team.objects.create(
            id='19538871',
            name='Manchester United',
            short_name='Manchester Utd',
        )
        self.away = models.Team.objects.create(
            id='822bd0ba',
            name='Liverpool',
            short_name='Liverpool',
        )

    def test_create_new_fixture(self):
        self._create_fixture()

    def test_id_must_be_unique(self):
        self._create_fixture()
        with self.assertRaises(IntegrityError):
            self._create_fixture()

    def test_id_required(self):
        with self.assertRaises(IntegrityError):
            self._create_fixture(id=None)

    def test_competition_required(self):
        with self.assertRaises(IntegrityError):
            self._create_fixture(competition=None)

    def test_season_required(self):
        with self.assertRaises(IntegrityError):
            self._create_fixture(season=None)

    def test_date_required(self):
        with self.assertRaises(IntegrityError):
            self._create_fixture(date=None)

    def test_time_not_required(self):
        self._create_fixture(time=None)
        self.assertEqual(len(models.Fixture.objects.all()), 1)

    def test_home_required(self):
        with self.assertRaises(IntegrityError):
            self._create_fixture(home=None)

    def test_away_required(self):
        with self.assertRaises(IntegrityError):
            self._create_fixture(away=None)

    def test_goals_home_not_required(self):
        self._create_fixture(goals_home=None)
        self.assertEqual(len(models.Fixture.objects.all()), 1)

    def test_goals_away_not_required(self):
        self._create_fixture(goals_away=None)
        self.assertEqual(len(models.Fixture.objects.all()), 1)

    def test_xG_home_not_required(self):
        self._create_fixture(xG_home=None)
        self.assertEqual(len(models.Fixture.objects.all()), 1)

    def test_xG_away_not_required(self):
        self._create_fixture(xG_away=None)
        self.assertEqual(len(models.Fixture.objects.all()), 1)

    def test_home_relates_to_team(self):
        self._create_fixture()
        fixture = models.Fixture.objects.get(id="e62685d4")
        self.assertEqual(fixture.home, self.home)

    def test_away_relates_to_team(self):
        self._create_fixture()
        fixture = models.Fixture.objects.get(id="e62685d4")
        self.assertEqual(fixture.away, self.away)

    def test_string_representation(self):
        self._create_fixture()
        fixture = models.Fixture.objects.get(id="e62685d4")
        expected = "2021-08-14 Premier League: Manchester Utd 0-5 Liverpool"
        self.assertEqual(expected, str(fixture))
