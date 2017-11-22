from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^loggedin$', views.loggedin),
    url(r'^items/add$', views.additem),
    url(r'^additem/(?P<number>\d+)/add$', views.itemadded),
    url(r'^wishitem/(?P<number>\d+)/wish$', views.wishadd),
    url(r'^item/(?P<number>\d+)/remove$', views.remove),
    url(r'^item/(?P<number>\d+)/show$', views.show),
    url(r'^remove/(?P<number>\d+)/delete$', views.delete),
    url(r'^logout$', views.logout),
]
