from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from VKstorage.models import Groups, Posts
from VKstorage.serializers import AactivityInGroupsSerializer, PostsSerializer

# @login_required
def index(request):
    zacup_list = Groups.objects.all().exclude(id=20)
    content = {
        'title': 'Академия закупок Алексея Дитриха',
        'zacup_list': zacup_list
    }
    return render(request, 'VKstorage/index.html', content)# Create your views here.


class AactivityInGroupsView(ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = AactivityInGroupsSerializer

class PostsView(ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
