from django.urls import path
from rest_framework.routers import SimpleRouter
from VKstorage import views

router = SimpleRouter()
router.register('api/activityingroups', views.AactivityInGroupsView, basename='activityingroups')
router.register('api/reportgroups', views.MonthlyReportView, basename='reportgroups')
router.register('api/posts', views.PostsView)
router.register('api/groups', views.GroupsView, basename='groups')

urlpatterns = [
    path('', views.index, name='home'),
    path('groups', views.all_groups, name='groups'),
]

urlpatterns += router.urls
