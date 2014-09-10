from django.conf.urls import patterns, url

import learn.views


urlpatterns = patterns(
    '',
    url("(?P<tutorial>how-to-make-a-polynomial-fit)/$",
        learn.views.data_literacy_template),
    url("(?P<tutorial>basic-statistics-tutorial)/$",
        learn.views.data_literacy_template)
)
