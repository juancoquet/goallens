from django.db import models


class Team(models.Model):
    id = models.CharField(max_length=16, primary_key=True, default=None)
    name = models.CharField(max_length=45)
    short_name = models.CharField(max_length=25)
    
    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name