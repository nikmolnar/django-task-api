from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from task_api.views import TaskInfoViewSet

router = DefaultRouter()
router.register(r'tasks', TaskInfoViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls))
]
