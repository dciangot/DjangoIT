from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^(?P<question_id>[\w]+)$', views.index, name='detail'),
            ]
