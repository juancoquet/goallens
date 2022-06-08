import os
import requests
import shutil

from data_sourcing.models import Team


team_ids = Team.objects.values_list('id', flat=True)

def download_image(team_id):
    if not os.path.isfile(f'static/images/team_logos/{team_id}.png'):
        print(f'Downloading image for team {team_id}')
        url = f'https://d2p3bygnnzw9w3.cloudfront.net/req/202205232/tlogo/fb/{team_id}.png'
        response = requests.get(url, stream=True)
        with open(f'static/images/team_logos/{team_id}.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)


def run():
    for team_id in team_ids:
        download_image(team_id)