# Generated by Django 4.0.4 on 2022-05-24 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.CharField(default=None, max_length=16, primary_key=True, serialize=False),
        ),
    ]
