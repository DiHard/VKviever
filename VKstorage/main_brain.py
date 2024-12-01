import os, sys
import datetime
import time
from time import sleep

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VKviewer.settings")

import django
django.setup()

import requests
from VKstorage.models import Settings, Stories, Groups, Posts


def refresh_token():
    setting = Settings.objects.get(id=1)

    url = f"https://id.vk.com/oauth2/auth?grant_type=refresh_token&client_id={setting.client_id}&device_id={setting.device_id}&state={setting.state}"
    response = requests.post(url, data={"refresh_token": setting.refresh_token})
    result = response.json()
    print(result)
    setting.refresh_token = result['refresh_token']
    setting.access_token = result['access_token']
    setting.save()
    print("Новый токен получен и сохранен.")


def get_stories():
    setting = Settings.objects.get(id=1)
    url = "https://api.vk.com/method/stories.get"
    params = {
        "access_token": setting.access_token,
        "v": setting.vkapi_version
        }
    response = requests.get(url, params=params)
    result = response.json()
    # print(result)

    if result['response']['count']==0:
        print('Нет сторис доступных к просмотру')
    else:
        groups = result['response']['items']
        for group in groups:
            stories = group['stories']
            for story in stories:
                if not Stories.objects.filter(story_id=story['id']).exists():
                    if Groups.objects.filter(group_id=story['owner_id'] * -1).exists():
                        new_story = Stories()
                        new_story.story_id = story['id']
                        new_story.group = Groups.objects.get(group_id=story['owner_id'] * -1)
                        new_story.date = datetime.datetime.fromtimestamp(story['date'])
                        new_story.unix_date = story['date']
                        new_story.story_type = story['type']
                        new_story.save()
                        print("Информация о сторис получена")



def get_posts(short_name, count):
    setting = Settings.objects.get(id=1)
    url = "https://api.vk.com/method/wall.get"
    params = {
        "access_token": setting.access_token,
        "count": count,
        "domain": short_name,
        "v": setting.vkapi_version
        }
    response = requests.get(url, params=params)
    result = response.json()
    # print(result)
    if result['response']['count']==0:
        print('Нет записей, доступных к просмотру')
    else:
        items = result['response']['items']
        # print(items)
        # print('------')
        for item in items:
            if item['attachments']: attachments = item['attachments']
            if Posts.objects.filter(post_id=item['id']).exists():
                post = Posts.objects.get(post_id=item['id'])
                post.likes = item['likes']['count']
                post.comments = item['comments']['count']
                post.reposts = item['reposts']['count']
                post.views = item['views']['count']
                post.text = (item['text'])[0:50]
                type_power = 0
                if item['attachments']:
                    for attachment in attachments:
                        if attachment['type'] == 'video':
                            if attachment['video']['type'] == 'short_video':
                                type_power = 2
                                post.post_type = 3
                            elif attachment['video']['type'] == 'video':
                                if type_power<2:
                                    type_power = 1
                                    post.post_type = 1
                        elif attachment['type'] == 'link':
                            if type_power < 1:
                                type_power = 1
                                post.post_type = 4
                        else:
                            if type_power < 1:
                                post.post_type = 2
                else:
                    post.post_type = 2
                post.save()
            else:
                # print('Сохраняем новый пост!')
                # print(item)
                post = Posts()
                post.post_id = item['id']
                post.group = Groups.objects.get(group_id=item['owner_id'] * -1)
                post.date = datetime.datetime.fromtimestamp(item['date'])
                post.unix_date = item['date']
                post.likes = item['likes']['count']
                post.comments = item['comments']['count']
                post.reposts = item['reposts']['count']
                post.views = item['views']['count']
                post.text = (item['text'])[0:50]
                type_power = 0
                # TO DO этот кусок можно вывести в функцию
                if item['attachments']:
                    for attachment in attachments:
                        if attachment['type'] == 'video':
                            if attachment['video']['type'] == 'short_video':
                                type_power = 2
                                post.post_type = 3
                            elif attachment['video']['type'] == 'video':
                                if type_power<2:
                                    type_power = 1
                                    post.post_type = 1
                        elif attachment['type'] == 'link':
                            if type_power < 1:
                                type_power = 1
                                post.post_type = 4
                        else:
                            if type_power < 1:
                                post.post_type = 2
                else:
                    post.post_type = 2
                post.save()


refresh_time = 0
nomer = 1
while True:
    print(f"Начинаем цикл № {nomer}")
    all_groups = Groups.objects.all()
    if refresh_time+2700 < int(time.time()):
        refresh_token()
        refresh_time = int(time.time())
        sleep(1)
    for group in all_groups:
        if group.last_update < datetime.date.today():
            count = 100
        else:
            count = 20
        print(f' - Для {group.short_name} запрашиваем {count} постов')
        group.last_update = datetime.date.today()
        group.save()
        get_posts(group.short_name, count)
        sleep(2)
    get_stories()
    print(f"Завершен цикл № {nomer}. Пауза 10 секунд")
    print("-- -- -- -- --")
    nomer += 1
    sleep(10)
