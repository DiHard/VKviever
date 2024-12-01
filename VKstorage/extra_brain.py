from VKstorage.models import Settings
import requests


def get_group_data(short_name):
    setting = Settings.objects.get(id=1)
    url = "https://api.vk.com/method/groups.getById"
    params = {
        "access_token": setting.access_token,
        "group_id": short_name,
        "v": setting.vkapi_version
        }
    response = requests.get(url, params=params)
    result = response.json()
    print(result)
    return result