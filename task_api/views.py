from rest_framework import mixins, viewsets

from task_api.models import TaskInfo
from task_api.serializers import TaskInfoSerializer


class TaskInfoViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = TaskInfo.objects.all()
    serializer_class = TaskInfoSerializer
    lookup_field = 'uuid'
