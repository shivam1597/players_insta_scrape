import requests
from bs4 import BeautifulSoup
from time import sleep
import cloudinary.uploader

cloudinary.config(
            cloud_name="shivam1519",
            api_key="854775435856326",
            api_secret="HvYInSsrqgYDlL0t8ILlS2H-mqk"
        )
response = requests.get('https://www.cricbuzz.com/cricket-team/india/2/players')

soup = BeautifulSoup(response.text, 'html.parser')
elements = soup.find_all(class_="cb-sub-lg-sec")

all_teams_url = []

all_players_name = []
for element in elements:
    sub_element = element.find(class_='cb-sub-lg-sec-head')
    if sub_element.text == 'Test Teams':
        player_elements = element.find_all(class_='cb-subnav-item cb-sub-lg-sec-item')
        for player_element in player_elements:
            dict_to_add = {'href': player_element['href'], 'country_name': player_element.text}
            all_teams_url.append(dict_to_add)

sleep(2)

cricbuzz_players_info_list = []
for team_url in all_teams_url:
    player_name_search_response = requests.get('https://www.cricbuzz.com{}/players'.format(team_url.get('href')))
    soup = BeautifulSoup(player_name_search_response.text, 'html.parser')
    player_div = soup.find_all(class_="cb-col cb-col-50")
    for div in player_div:
        img_element = div.find('img')
        img_url = img_element['src']
        name_element = div.find(class_="cb-font-16 text-hvr-underline")
        player_profile_url = div['href']
        player_dict_to_add = {'country': team_url.get('country_name'), 'player_name': name_element.text,
                              'player_image': 'https://www.cricbuzz.com{}'.format(img_url), 'profile_url': 'https://www.cricbuzz.com{}'.format(player_profile_url)}
        cricbuzz_players_info_list.append(player_dict_to_add)

instagram_profile_list = []
for cricbuzz_player in cricbuzz_players_info_list:
    google_search_response = requests.get('https://www.google.com/search?q=instagram%3A+{}'.format(cricbuzz_player.get('player_name').replace(' ','+')))
    google_soup = BeautifulSoup(google_search_response.text, 'html.parser')
    parent_element = google_soup.find(class_='egMi0 kCrYT')
    link_element = parent_element.find('a')
    instagram_map_to_add = {
        'country': cricbuzz_player.get('country'),
        'player_name': cricbuzz_player.get('player_name'),
        'player_image': cricbuzz_player.get('player_image'),
        'profile_url': cricbuzz_player.get('profile_url'),
        'instagram_profile': link_element['href'].replace('/url?q=', '')
    }
    instagram_profile_list.append(instagram_map_to_add)
    sleep(4)

with open('insta_list.txt', mode='w+', encoding='utf-8', errors='ignore') as f:
    f.write(str(instagram_profile_list))
        
with open('insta_list.txt', mode='r+', encoding='utf-8', errors='ignore') as f:
    cloudinary.uploader.upload(f.name, resource_type='raw', use_filename=True,
                                unique_filename=False)