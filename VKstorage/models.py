from django.db import models

class Settings(models.Model):
    refresh_token = models.TextField('Refresh token')
    access_token = models.TextField('Access token')
    client_id = models.CharField('Client id', max_length=250)
    device_id = models.CharField('Device id', max_length=250)
    state = models.CharField('State', max_length=250)
    scope = models.CharField('Scope (список доступов)', max_length=250)
    vkapi_version = models.CharField('Версия VK API', max_length=250)
    last_full_update = models.DateField('Дата последнего полного обновления')

    def __str__(self):
        return "Ключевые настройки сервиса"

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"


class Groups(models.Model):
    name = models.CharField('Название группы', max_length=250)
    group_id = models.CharField('Groups id', max_length=250)
    short_name = models.CharField('Короткое имя', max_length=250)
    last_update = models.DateField('Дата последнего полного информации о группе')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Stories(models.Model):
    story_id = models.CharField('Groups id', max_length=250)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    start_date = models.CharField('Groups id', max_length=250)
    story_type = models.CharField('Groups id', max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"