from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from VKstorage.models import Stories, Posts, Groups


class GroupsSerializer(ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'

class PostsSerializer(ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'

class StoriesSerializer(ModelSerializer):
    class Meta:
        model = Stories
        fields = '__all__'

class AactivityInGroupsSerializer(ModelSerializer):
    # groups = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    stories = serializers.SerializerMethodField()
    class Meta:
        model = Groups
        fields = ['id', 'name', 'posts', 'stories']

    def get_posts(self, obj):
        queryset = Posts.objects.filter(group=obj)
        return [PostsSerializer(q).data for q in queryset]

    def get_stories(self, obj):
        queryset = Stories.objects.filter(group=obj)
        return [StoriesSerializer(q).data for q in queryset]