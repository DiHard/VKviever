from datetime import datetime
import time
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from VKstorage.extra_brain import get_group_data
from VKstorage.models import Stories, Posts, Groups

class GroupsSerializer(ModelSerializer):
    class Meta:
        model = Groups
        fields = ['id', 'name', 'short_name']

    def validate_name(self, value):
        short_name = value[9 + (value[8:99].find('/')):99]
        data = get_group_data(short_name)
        if 'error' in data:
            if 'error_msg' in data['error']:
                raise ValidationError(f"Ошибка получения данных о группе: {data['error']['error_msg']}")
            else:
                raise ValidationError("Ошибка получения данных о группе.")
        if Groups.objects.filter(short_name=short_name).exists():
            raise ValidationError("Ссылка на группу уже была добавлена прежде.")
        if value[0:8] != "https://":
            raise ValidationError("Ссылка на группу должна начинаться с https://")
        if value.count('/') > 4:
            raise ValidationError("Данный вид ссылок не поддерживается")
        return value

    def create(self, validated_data):
        instance = Groups(**validated_data)
        print('Сериалайзер в действии')
        print(validated_data)
        data = get_group_data(validated_data['name'][9 + (validated_data['name'][8:99].find('/')):99])
        data = data['response']['groups'][0]
        print(data)
        instance.name = data['name']
        instance.group_id = data['id']  # Устанавливаем значение вручную
        instance.short_name = data['screen_name']  # Устанавливаем значение вручную
        instance.last_update = '2024-01-01'  # Устанавливаем значение вручную
        instance.save()
        return instance

class PostsSerializer(ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'

class StoriesSerializer(ModelSerializer):
    class Meta:
        model = Stories
        fields = '__all__'

class AactivityInGroupsSerializer(ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    stories_count = serializers.SerializerMethodField()
    class Meta:
        model = Groups
        fields = ['id', 'name', 'short_name', 'posts_count', 'stories_count']

    def get_posts_count(self, obj):
        date_from = self.context['view'].request.query_params.get('from')
        date_to = self.context['view'].request.query_params.get('to')
        queryset = Posts.objects.filter(group=obj).filter(unix_date__gte=date_from).filter(unix_date__lte=date_to)
        posts = {'video': 0, 'photo': 0, 'short_video': 0, 'link': 0}
        for q in queryset:
            if q.post_type == 1: posts['video'] += 1
            if q.post_type == 2: posts['photo'] += 1
            if q.post_type == 3: posts['short_video'] += 1
            if q.post_type == 4: posts['link'] += 1
        return posts

    def get_stories_count(self, obj):
        date_from = self.context['view'].request.query_params.get('from')
        date_to = self.context['view'].request.query_params.get('to')
        return Stories.objects.filter(group=obj).filter(unix_date__gte=date_from).filter(unix_date__lte=date_to).count()


class MonthlyReportSerializer(ModelSerializer):
    monthly_report = serializers.SerializerMethodField()
    class Meta:
        model = Groups
        fields = ['id', 'name', 'short_name', 'monthly_report']

    def get_monthly_report(self, obj):
        date_from = self.context['view'].request.query_params.get('from')
        date_to = self.context['view'].request.query_params.get('to')
        group = self.context['view'].request.query_params.get('group')
        posts = Posts.objects.filter(group__short_name=group).filter(unix_date__gte=date_from).filter(unix_date__lte=date_to).order_by('date')
        stories = Stories.objects.filter(group__short_name=group).filter(unix_date__gte=date_from).filter(unix_date__lte=date_to)
        next_day = int(date_from)
        monthly_report = {}
        while next_day < int(date_to):
            monthly_report.update({f'{next_day}': {'video': 0, 'photo': 0, 'short_video': 0, 'link': 0, 'stories': 0}})
            next_day += 86400
        for q in posts:
            if q.post_type == 1:
                for el in monthly_report:
                    if int(el) <= int(q.unix_date) < int(el)+86400: monthly_report[f'{el}']['video'] += 1
            if q.post_type == 2:
                for el in monthly_report:
                    if int(el) <= int(q.unix_date) < int(el) + 86400: monthly_report[f'{el}']['photo'] += 1
            if q.post_type == 3:
                for el in monthly_report:
                    if int(el) <= int(q.unix_date) < int(el) + 86400: monthly_report[f'{el}']['short_video'] += 1
            if q.post_type == 4:
                for el in monthly_report:
                    if int(el) <= int(q.unix_date) < int(el) + 86400: monthly_report[f'{el}']['link'] += 1
        for q in stories:
            for el in monthly_report:
                if int(el) <= int(q.unix_date) < int(el) + 86400: monthly_report[f'{el}']['stories'] += 1
        monthly_report_ru = {}
        for el in reversed(monthly_report):
            day = time.strftime("%d %B %Y %H:%M:%S", time.localtime(int(el)))
            months = {
                "January": "января",
                "February": "февраля",
                "March": "марта",
                "April": "апреля",
                "May": "мая",
                "June": "июня",
                "July": "июля",
                "August": "августа",
                "September": "сентября",
                "October": "октября",
                "November": "ноября",
                "December": "декабря",
            }
            for en, ru in months.items():
                day = day.replace(en, ru)
            monthly_report_ru.update({day: monthly_report[el]})
        return monthly_report_ru