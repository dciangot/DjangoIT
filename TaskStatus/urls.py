from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^(?P<doc_id>[\S]+)$', views.document, name='document'),
            ]
