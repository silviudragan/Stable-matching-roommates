from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<token>[0-9a-zA-Z]+)/$', views.index, name='index'),
    url(r'^profil/(?P<token>[0-9a-zA-Z]+)/$', views.Profil.as_view(), name='profil'),
    url(r'^recenzie/(?P<token>[0-9a-zA-Z]+)/$', views.Recenzii.as_view(), name='recenzie'),
]

