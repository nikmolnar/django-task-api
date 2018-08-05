from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter

from task_api.views import TaskInfoViewSet

router = SimpleRouter()
router.register(r'tasks', TaskInfoViewSet)

urlpatterns = [
    url(r'^/', include(router.urls, namespace='task-api'))
]
