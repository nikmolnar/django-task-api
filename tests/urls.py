from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('task_api.urls')),
]
