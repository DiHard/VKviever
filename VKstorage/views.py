from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from VKstorage.models import Groups, Posts
from VKstorage.serializers import AactivityInGroupsSerializer, PostsSerializer, GroupsSerializer, \
    MonthlyReportSerializer


@login_required
def index(request):
    return render(request, 'VKstorage/index.html', {'title': 'Формирование отчета'})# Create your views here.
@login_required
def monthly_report(request, pk):
    group = Groups.objects.get(short_name=pk)
    context = {'title': 'Месячный отчет по группе', 'short_name': pk, 'group': group}
    return render(request, 'VKstorage/monthly_report.html', context)# Create your views here.
@login_required
def all_groups(request):
    return render(request, 'VKstorage/groups.html', {'title': 'Управление пабликами'})# Create your views here.

class AactivityInGroupsView(ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = AactivityInGroupsSerializer
    permission_classes = [permissions.IsAuthenticated]

class MonthlyReportView(ModelViewSet):
    # queryset = Groups.objects.all()
    serializer_class = MonthlyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        short_name = self.request.query_params.get('group')
        print(short_name)
        queryset = Groups.objects.filter(short_name=short_name)
        return queryset

class PostsView(ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupsView(ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer
    permission_classes = [permissions.IsAuthenticated]
