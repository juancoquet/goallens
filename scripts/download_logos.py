import os
from PIL import Image
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

def clear_background(team_id):
    if not os.path.isfile(f'static/images/team_logos/{team_id}.png'):
        raise ImageDoesNotExist(f'{team_id}.png does not exist')

    bitmap = _create_binary_bitmap(team_id)
    bitmap = bfs_bitmap(bitmap)
    img = Image.open(f'static/images/team_logos/{team_id}.png').convert('RGBA')
    data = img.getdata()
    new_data = []
    width, height = img.size
    for r in range(height):
        for c in range(width):
            if bitmap[r][c] == 2:
                # clear the pixel
                new_data.append((255, 255, 255, 0))
            else:
                # keep the pixel
                pixel = data[r * width + c]
                new_data.append(pixel)
    img.putdata(new_data)
    img.save(f'static/images/team_logos/{team_id}.png')

def _create_binary_bitmap(team_id):
    """creates a binary bitmap of a team's logo image, where 1 represents
    a white pixel and 0 a non-white pixel.

    Args:
        team_id (str): the team's id
    """
    if not os.path.isfile(f'static/images/team_logos/{team_id}.png'):
        raise ImageDoesNotExist(f'{team_id}.png does not exist')

    img = Image.open(f'static/images/team_logos/{team_id}.png').convert('RGBA')
    data = img.getdata()
    width, height = img.size
    bitmap = []
    for y in range(height):
        row = []
        for x in range(width):
            pixel = data[y * width + x]
            if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
                row.append(1)
            else:
                row.append(0)
        bitmap.append(row)
    return bitmap

def bfs_bitmap(bitmap):
    """performs a bfs on a binary bitmap starting from each pixel in the perimeter
    of the bitmap. If a 1 pixel is connected to the perimiter, it is changed to a 2."""
    width, height = len(bitmap[0]), len(bitmap)
    steps = ((1, 0), (0, 1), (-1, 0), (0, -1))

    top_row_indexes = [(0, i) for i in range(width)]
    bottom_row_indexes = [(height - 1, i) for i in range(width)]
    left_column_indexes = [(i, 0) for i in range(height)]
    right_column_indexes = [(i, width - 1) for i in range(height)]
    
    visited = []
    to_visit = top_row_indexes + bottom_row_indexes + left_column_indexes + right_column_indexes

    while to_visit:
        curr = to_visit.pop(0)
        if curr in visited:
            continue
        visited.append(curr)
        if bitmap[curr[0]][curr[1]] == 1:
            bitmap[curr[0]][curr[1]] = 2
            for step in steps:
                new_r = curr[0] + step[0]
                new_c = curr[1] + step[1]
                if 0 <= new_r < height and 0 <= new_c < width:
                    to_visit.append((new_r, new_c))
    return bitmap


class ImageDoesNotExist(Exception):
    pass


def run():
    for team_id in team_ids:
        print(f'processing team {team_id}')
        download_image(team_id)
        bitmap = _create_binary_bitmap(team_id)
        bitmap = bfs_bitmap(bitmap)
        clear_background(team_id)