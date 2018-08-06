from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from task_api.views import TaskInfoViewSet

router = DefaultRouter()
router.register(r'tasks', TaskInfoViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
