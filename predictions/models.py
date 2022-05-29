from django.db import models

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
    prob_ag_0 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_1 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_2 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_3 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_4 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_5 = models.DecimalField(max_digits=4, decimal_places=2)
    prob_ag_6 = models.DecimalField(max_digits=4, decimal_places=2)
    likely_hg = models.SmallIntegerField()
    likely_ag = models.SmallIntegerField()

    class Meta:
        db_table = 'predictions'

    def __str__(self):
        return f'prediction {self.likely_hg}-{self.likely_ag} {self.fixture.id}: {self.fixture}'