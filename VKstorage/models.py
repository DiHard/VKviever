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
    story_id = models.CharField('Story id', max_length=250)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    date = models.DateTimeField('Дата и время публикации')
    unix_date = models.IntegerField('Дата и время публикации UNIX')
    story_type = models.CharField('Тип публикации', max_length=250)

    def __str__(self):
        return self.story_id + " - " + self.group.name

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"


class Posts(models.Model):
    POST_TYPE_CHOICES = (
        (1, 'Видео'),
        (2, 'Пост'),
        (3, 'Репост клипа'),
        (4, 'Статья'),
    )
    post_id = models.CharField('Пост id', max_length=250)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    date = models.DateTimeField('Дата и время публикации')
    unix_date = models.IntegerField('Дата и время публикации UNIX')
    post_type = models.IntegerField('Тип публикации', choices=POST_TYPE_CHOICES)
    likes = models.IntegerField("Лийки")
    comments = models.IntegerField("Коментарии")
    reposts = models.IntegerField("Репосты")
    views = models.IntegerField("Просмотры")
    text = models.CharField('Краткий текст поста', max_length=250)


    def __str__(self):
        return str(self.post_type) + " - " + self.group.name + " - Дата: " + str(self.start_date) + " - " + str(self.text)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"