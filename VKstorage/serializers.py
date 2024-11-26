from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from VKstorage.models import Stories, Posts, Groups

class PostsSerializer(ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'

class StoriesSerializer(ModelSerializer):
    class Meta:
        model = Stories
        fields = '__all__'

class AactivityInGroupsSerializer(ModelSerializer):
    posts = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    stories = serializers.SerializerMethodField()
    stories_count = serializers.SerializerMethodField()
    class Meta:
        model = Groups
        fields = ['id', 'name', 'posts_count', 'stories_count', 'posts', 'stories']

    def get_posts(self, obj):
        date_from = self.context['view'].request.query_params.get('from')
        date_to = self.context['view'].request.query_params.get('to')
        print(self.context['view'].request.query_params)
        queryset = Posts.objects.filter(group=obj).filter(start_date__gte=date_from).filter(start_date__lte=date_to)
        return [PostsSerializer(q).data for q in queryset]

    def get_posts_count(self, obj):
        date_from = self.context['view'].request.query_params.get('from')
        queryset = Posts.objects.filter(group=obj).filter(start_date__gte=date_from)
        posts = {'video': 0, 'photo': 0, 'short_video': 0, 'link': 0}
        for q in queryset:
            if q.post_type == 1: posts['video'] += 1
            if q.post_type == 2: posts['photo'] += 1
            if q.post_type == 3: posts['short_video'] += 1
            if q.post_type == 4: posts['link'] += 1
        return posts

    def get_stories(self, obj):
        queryset = Stories.objects.filter(group=obj)
        return [StoriesSerializer(q).data for q in queryset]

    def get_stories_count(self, obj):
        return Stories.objects.filter(group=obj).count()
