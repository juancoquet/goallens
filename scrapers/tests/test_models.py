from unicodedata import name
from django.db.utils import IntegrityError
from django.test import TestCase, TransactionTestCase

from scrapers import models


class TestTeamModel(TransactionTestCase):

    def setUp(self):
        models.Team.objects.create(
            id='19538871',
            name='Manchester United',
            short_name='Manchester Utd',
        )

    def tearDown(self):
        models.Team.objects.all().delete()

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


class TestFixtureModel(TestCase):

    def setUp(self):
        models.Team.objects.create(
            id='19538871',
            name='Manchester United',
            short_name='Manchester Utd',
        )
        models.Team.objects.create(
            id='822bd0ba',
            name='Liverpool',
            short_name='Liverpool',
        )

    def tearDown(self):
        models.Fixture.objects.all().delete()
        models.Team.objects.all().delete()

    def test_create_new_fixture(self):
        models.Fixture.objects.create(
            id="e62685d4",
            competition="Premier League",
            season="2021-2022",
            date="2021-08-14",
            time="12:30:00",
            home_id="19538871",
            away_id="822bd0ba",
            status="FINISHED",
            goals_home=0,
            goals_away=5,
            xG_home=1.5,
            xG_away=3.8,
        )

    def test_id_must_be_unique(self):
        models.Fixture.objects.create(
            id="e62685d4",
            competition="Premier League",
            season="2021-2022",
            date="2021-08-14",
            time="12:30:00",
            home_id="19538871",
            away_id="822bd0ba",
            status="FINISHED",
            goals_home=0,
            goals_away=5,
            xG_home=1.5,
            xG_away=3.8,
        )
        with self.assertRaises(IntegrityError):
            models.Fixture.objects.create(
                id="e62685d4",
                competition="Premier League",
                season="2021-2022",
                date="2021-08-14",
                time="12:30:00",
                home_id="19538871",
                away_id="822bd0ba",
                status="FINISHED",
                goals_home=0,
                goals_away=5,
                xG_home=1.5,
                xG_away=3.8,
            )

    def test_id_required(self):
        with self.assertRaises(IntegrityError):
            models.Fixture.objects.create(
                competition="Premier League",
                season="2021-2022",
                date="2021-08-14",
                time="12:30:00",
                home_id="19538871",
                away_id="822bd0ba",
                status="FINISHED",
                goals_home=0,
                goals_away=5,
                xG_home=1.5,
                xG_away=3.8,
            )

    def test_competition_required(self):
        with self.assertRaises(IntegrityError):
            models.Fixture.objects.create(
                id="e62685d4",
                season="2021-2022",
                date="2021-08-14",
                time="12:30:00",
                home_id="19538871",
                away_id="822bd0ba",
                status="FINISHED",
                goals_home=0,
                goals_away=5,
                xG_home=1.5,
                xG_away=3.8,
            )

    def test_season_required(self):
        with self.assertRaises(IntegrityError):
            models.Fixture.objects.create(
                id="e62685d4",
                competition="Premier League",
                date="2021-08-14",
                time="12:30:00",
                home_id="19538871",
                away_id="822bd0ba",
                status="FINISHED",
                goals_home=0,
                goals_away=5,
                xG_home=1.5,
                xG_away=3.8,
            )

    def test_date_required(self):
        with self.assertRaises(IntegrityError):
            models.Fixture.objects.create(
                id="e62685d4",
                competition="Premier League",
                season="2021-2022",
                time="12:30:00",
                home_id="19538871",
                away_id="822bd0ba",
                status="FINISHED",
                goals_home=0,
                goals_away=5,
                xG_home=1.5,
                xG_away=3.8,
            )

    def test_time_not_required(self):
        models.Fixture.objects.create(
            id="e62685d4",
            competition="Premier League",
            season="2021-2022",
            date="2021-08-14",
            home_id="19538871",
            away_id="822bd0ba",
            status="FINISHED",
            goals_home=0,
            goals_away=5,
            xG_home=1.5,
            xG_away=3.8,
        )
        self.assertEqual(len(models.Fixture.objects.all()), 1)

    def test_home_id_required(self):
        with self.assertRaises(IntegrityError):
            models.Fixture.objects.create(
                id="e62685d4",
                competition="Premier League",
                season="2021-2022",
                date="2021-08-14",
                time="12:30:00",
                away_id="822bd0ba",
                status="FINISHED",
                goals_home=0,
                goals_away=5,
                xG_home=1.5,
                xG_away=3.8,
            )

    def test_away_id_required(self):
        with self.assertRaises(IntegrityError):
            models.Fixture.objects.create(
                id="e62685d4",
                competition="Premier League",
                season="2021-2022",
                date="2021-08-14",
                time="12:30:00",
                home_id="19538871",
                status="FINISHED",
                goals_home=0,
                goals_away=5,
                xG_home=1.5,
                xG_away=3.8,
            )

    def test_status_required(self):
        with self.assertRaises(IntegrityError):
            models.Fixture.objects.create(
                id="e62685d4",
                competition="Premier League",
                season="2021-2022",
                date="2021-08-14",
                time="12:30:00",
                home_id="19538871",
                away_id="822bd0ba",
                goals_home=0,
                goals_away=5,
                xG_home=1.5,
                xG_away=3.8,
            )

    def test_goals_home_not_required(self):
        models.Fixture.objects.create(
            id="e62685d4",
            competition="Premier League",
            season="2021-2022",
            date="2021-08-14",
            time="12:30:00",
            home_id="19538871",
            away_id="822bd0ba",
            status="FINISHED",
            goals_away=5,
            xG_home=1.5,
            xG_away=3.8,
        )
        self.assertEqual(len(models.Fixture.objects.all()), 1)

    def test_goals_away_not_required(self):
        models.Fixture.objects.create(
            id="e62685d4",
            competition="Premier League",
            season="2021-2022",
            date="2021-08-14",
            time="12:30:00",
            home_id="19538871",
            away_id="822bd0ba",
            status="FINISHED",
            goals_home=5,
            xG_home=1.5,
            xG_away=3.8,
        )
        self.assertEqual(len(models.Fixture.objects.all()), 1)

    def test_xG_home_not_required(self):
        models.Fixture.objects.create(
            id="e62685d4",
            competition="Premier League",
            season="2021-2022",
            date="2021-08-14",
            time="12:30:00",
            home_id="19538871",
            away_id="822bd0ba",
            status="FINISHED",
            goals_home=5,
            goals_away=5,
            xG_away=3.8,
        )
        self.assertEqual(len(models.Fixture.objects.all()), 1)

    def test_xG_away_not_required(self):
        models.Fixture.objects.create(
            id="e62685d4",
            competition="Premier League",
            season="2021-2022",
            date="2021-08-14",
            time="12:30:00",
            home_id="19538871",
            away_id="822bd0ba",
            status="FINISHED",
            goals_home=5,
            goals_away=5,
            xG_home=1.5,
        )
        self.assertEqual(len(models.Fixture.objects.all()), 1)