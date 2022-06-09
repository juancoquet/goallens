from django.db import models # type: ignore

from data_sourcing.models import Fixture


class Prediction(models.Model):
    id = models.AutoField(primary_key=True)
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    forecast_hxG = models.DecimalField(max_digits=4, decimal_places=2)
    forecast_axG = models.DecimalField(max_digits=4, decimal_places=2)
    prob_hg_0 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_hg_1 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_hg_2 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_hg_3 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_hg_4 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_hg_5 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_hg_6 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_hg_7 = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    prob_ag_0 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_1 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_2 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_3 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_4 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_5 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_6 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_7 = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    likely_hg = models.SmallIntegerField()
    likely_ag = models.SmallIntegerField()

    class Meta:
        db_table = 'predictions'

    def __str__(self):
        return f'prediction {self.likely_hg}-{self.likely_ag} {self.fixture.id}: {self.fixture}'

    @property
    def home_win_prob(self):
        prob = 0
        for hg in range(7):
            hg += 1
            hg_prob = getattr(self, f'prob_hg_{hg}')
            for ag in range(hg):
                ag_prob = getattr(self, f'prob_ag_{ag}')
                prob += hg_prob * ag_prob
        return prob

    @property
    def away_win_prob(self):
        prob = 0
        for ag in range(7):
            ag += 1
            ag_prob = getattr(self, f'prob_ag_{ag}')
            for hg in range(ag):
                hg_prob = getattr(self, f'prob_hg_{hg}')
                prob += hg_prob * ag_prob
        return prob

    @property
    def draw_prob(self):
        prob = 0
        for g in range(8):
            hg_prob = getattr(self, f'prob_hg_{g}')
            ag_prob = getattr(self, f'prob_ag_{g}')
            prob += hg_prob * ag_prob
        return prob