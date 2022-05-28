import csv

from data_sourcing.models import Team

def run():
    all_teams = Team.objects.all()
    with open('teams.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'team_name', 'team_short_name'])
        for team in all_teams:
            writer.writerow([team.id, team.name, team.short_name])