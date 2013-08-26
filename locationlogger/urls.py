from django.conf.urls import patterns, url

from locationlogger import views

urlpatterns = patterns('',
    url(r'^update/$', views.update_location, name='update_location'),
)