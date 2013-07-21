from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^lookup/$', views.ChosenLookup.as_view(), name='chosen_lookup'), 
)

