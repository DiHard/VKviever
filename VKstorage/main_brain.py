import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VKviewer.settings")

import django
django.setup()

import requests
from VKstorage.models import Settings

def refresh_token():
    setting = Settings.objects.get(id=1)

    url = f"https://id.vk.com/oauth2/auth?grant_type=refresh_token&client_id={setting.client_id}&device_id={setting.device_id}&state={setting.state}"
    response = requests.post(url, data={"refresh_token": setting.refresh_token})
    result = response.json()
    print(result)
    setting.refresh_token = result['refresh_token']
    setting.access_token = result['access_token']
    setting.save()


refresh_token()

def get_stories():
    setting = Settings.objects.get(id=1)
    url = "https://api.vk.com/method/stories.get"
    params = {
        "access_token": setting.access_token,
        "v": setting.vkapi_version
        }
    response = requests.post(url, params=params)
    result = response.json()
    print(result)

    if result['response']['count']==0:
        print('Нет сторис доступных к просмотру')
    else:
        groups = result['response']['items']
        for group in groups:
            print('------')
            stories = group['stories']
            for story in stories:
                print(group['name'])
                print(story['id'])
                print(story['owner_id'])
                print(story['date'])
                print(story['type'])


get_stories()