from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from VKstorage.models import Groups, Posts
from VKstorage.serializers import AactivityInGroupsSerializer, PostsSerializer, GroupsSerializer


@login_required
def index(request):
    return render(request, 'VKstorage/index.html', {'title': 'Формирование отчета'})# Create your views here.
@login_required
def all_groups(request):
    return render(request, 'VKstorage/groups.html', {'title': 'Формирование отчета'})# Create your views here.

class AactivityInGroupsView(ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = AactivityInGroupsSerializer

class PostsView(ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

class GroupsView(ModelViewSet):
    print('Вью в действии')
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer