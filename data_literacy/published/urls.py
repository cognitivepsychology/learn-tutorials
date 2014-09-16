from django.conf.urls import patterns, url

import learn.views


urlpatterns = patterns(
    '',
    url("(?P<tutorial>basic-statistics-tutorial)/$",
        learn.views.data_literacy_template)
)
