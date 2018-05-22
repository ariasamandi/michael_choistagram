from django.conf.urls import url
from . import views
from django.conf import settings
from django.views.static import serve
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^add_photo$', views.add_photo),
    url(r'^add_friend/(?P<id>\d+)$', views.add_friend),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^purchase$', views.purchase),
    url(r'^prestripe$', views.prestripe),
    url(r'^stripe$', views.stripe),
    url(r'^purchase/process$', views.purchase_process),
    url(r'^logout$', views.logout),
]
