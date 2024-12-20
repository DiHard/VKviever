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


def get_stories(owner_id):
    setting = Settings.objects.get(id=1)
    url = "https://api.vk.com/method/stories.get"
    params = {
        "access_token": setting.access_token,
        "v": setting.vkapi_version,
        "owner_id": int(owner_id)*-1
        }
    response = requests.get(url, params=params)
    result = response.json()
    # print(result)
    if 'error' in result:
        print(' - ОШБИКА получения сторис!')
        print(result)
    elif result['response']['count'] == 0:
        print(' - Нет сторис доступных к просмотру')
    else:
        groups = result['response']['items']
        for one_group in groups:
            # print(one_group)
            stories = one_group['stories']
            for story in stories:
                if not Stories.objects.filter(story_id=story['id']).exists():
                    # if Groups.objects.filter(group_id=story['owner_id'] * -1).exists():
                    new_story = Stories()
                    new_story.story_id = story['id']
                    new_story.group = Groups.objects.get(group_id=story['owner_id'] * -1)
                    new_story.date = datetime.datetime.fromtimestamp(story['date'])
                    new_story.unix_date = story['date']
                    new_story.story_type = story['type']
                    new_story.save()
                    print(" - Информация о сторис получена")
                else:
                    print(f"   - Сторис id={story['id']} уже в базе")


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
    if 'error' in result:
        print(' - ОШБИКА получения постов!')
        print(result)
    elif result['response']['count']==0:
        print('Нет записей, доступных к просмотру')
    else:
        items = result['response']['items']
        for item in items:
            if item['attachments']: attachments = item['attachments']
            if Posts.objects.filter(post_id=item['id'], group__short_name=short_name).exists():
                post = Posts.objects.get(post_id=item['id'], group__short_name=short_name)
                post.text = (item['text'])[0:50]
                type_power = 0 # в этом участке кода я перебераю медиа вложения и определяю какой тип поста у нас
                if item['attachments']:
                    for attachment in attachments:
                        if attachment['type'] == 'video':
                            if attachment['video']['type'] == 'short_video':
                                type_power = 2 # type_power нужен для защиты от перезаписи значения
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
                post = Posts()
                post.post_id = item['id']
                post.group = Groups.objects.get(short_name=short_name)
                post.date = datetime.datetime.fromtimestamp(item['date'])
                post.unix_date = item['date']
                post.text = (item['text'])[0:50]
                type_power = 0 # в этом участке кода я перебераю медиа вложения и определяю какой тип поста у нас
                if item['attachments']:
                    for attachment in attachments:
                        if attachment['type'] == 'video':
                            if attachment['video']['type'] == 'short_video':
                                type_power = 2 # type_power нужен для защиты от перезаписи значения
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
    if len(all_groups):
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
            sleep(5)
            get_stories(group.group_id)
            sleep(5)
    print(f"Завершен цикл № {nomer}. Пауза 10 секунд")
    print("-- -- -- -- --")
    nomer += 1
    sleep(10)