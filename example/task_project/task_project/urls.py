from django.conf.urls import url
from django.urls import include
from django.views.generic import TemplateView

urlpatterns = [
    url('^$', TemplateView.as_view(template_name='example.html')),
    url('^', include('task_api.urls'))
]
