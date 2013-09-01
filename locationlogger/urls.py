from django.conf.urls import patterns, url

from locationlogger import views

urlpatterns = patterns('',
    url(r'^update/$', views.update_location, name='update_location'),
    url(r'^where_is_she_really/$', views.last_known_loc_accurate, name='last_known_loc_accurate'),
)