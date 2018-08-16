from django.conf import settings
from rest_framework import mixins, viewsets

from task_api.models import TaskInfo
from task_api.serializers import TaskInfoSerializer
from task_api.utils import resolve_class

AUTHENTICATION_CLASSES = getattr(settings, 'TASK_API_AUTHENTICATION_CLASSES', [])
PERMISSIONS_CLASSES = getattr(settings, 'TASK_API_PERMISSIONS_CLASSES', [])


class TaskInfoViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = TaskInfo.objects.all()
    serializer_class = TaskInfoSerializer
    lookup_field = 'uuid'
    authentication_classes = [resolve_class(x) for x in AUTHENTICATION_CLASSES]
    permission_classes = [resolve_class(x) for x in PERMISSIONS_CLASSES]
