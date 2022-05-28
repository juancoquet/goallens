from django.db import models


class Team(models.Model):
    id = models.CharField(max_length=16, primary_key=True, default=None)
    name = models.CharField(max_length=45)
    short_name = models.CharField(max_length=25)
    
    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Fixture(models.Model):

    id = models.CharField(max_length=16, primary_key=True, default=None)
    competition = models.CharField(max_length=45)
    season = models.CharField(max_length=45)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_id')
    away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_id')
    goals_home = models.SmallIntegerField(blank=True, null=True)
    goals_away = models.SmallIntegerField(blank=True, null=True)
    xG_home = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    xG_away = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'fixtures'

    def __str__(self):
        score = 'vs'
        if (self.goals_home is not None) and (self.goals_away is not None):
            score = f'{self.goals_home}-{self.goals_away}'
        return f'{self.date} {self.competition}: {self.home.short_name} {score} {self.away.short_name}'