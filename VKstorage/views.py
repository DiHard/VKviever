from rest_framework.viewsets import ModelViewSet

from VKstorage.models import Groups
from VKstorage.serializers import AactivityInGroupsSerializer


class AactivityInGroupsView(ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = AactivityInGroupsSerializer

