from rest_framework.routers import SimpleRouter

from VKstorage import views

router = SimpleRouter()
router.register('api/keywords', views.AactivityInGroupsView)

urlpatterns = [
    # path('', views.index, name='home'),
    # path('settings/', views.bot_settings, name='settings'),
    # path('users/', views.users, name='users')
]

urlpatterns += router.urls
