from django.conf.urls import patterns, url
from django.views.generic import RedirectView

import learn.views


urlpatterns = patterns(
    '',
    url(r'^errorbars/$',
        RedirectView.as_view(
            url='/how-to-make-a-graph-with-error-bars-online/',
            permanent=True)),
    url(r'^how-to-make-a-graph-with-error-bars/$',
        RedirectView.as_view(
            url='/how-to-make-a-graph-with-error-bars-online/',
            permanent=True)),
    url(r'^area-chart-tutorial/$',
        RedirectView.as_view(
            url='/how-to-make-an-area-chart-online/',
            permanent=True)),
    url(r'^embed/$',
        RedirectView.as_view(
            url='/how-to-embed-plotly-graphs-in-websites/',
            permanent=True)),
    url(r'^multiple-axes-tutorial/$',
        RedirectView.as_view(
            url='/how-to-make-a-graph-with-multiple-axes-online/',
            permanent=True)),
    url(r'^how-to-make-a-line-graph-and-scatter-plot/$',
        RedirectView.as_view(
            url='/how-to-make-a-line-graph-and-scatter-plot-online/',
            permanent=True)),
    url(r'^share-print/$',
        RedirectView.as_view(
            url='/how-to-share-and-print-plotly-graphs/',
            permanent=True))
)
