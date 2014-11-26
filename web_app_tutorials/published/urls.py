from django.conf.urls import patterns, url

import learn.views


urlpatterns = patterns(
    '',
    url("(?P<tutorial>add-data-to-the-plotly-grid)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-make-a-line-graph-and-scatter-plot-online)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-make-a-bar-chart-online)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-make-an-area-chart-online)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-make-a-histogram-online)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-make-a-box-plot-online)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-make-a-bubble-chart-online)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-make-a-heatmap-online)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-make-a-graph-with-error-bars-online)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-make-a-graph-with-multiple-axes-online)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-sign-up-to-plotly)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-embed-plotly-graphs-in-websites)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-share-and-print-plotly-graphs)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-make-a-3d-line-chart-online)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>how-to-make-a-3d-scatter-plot-online)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>date-format-and-time-series)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>LaTeX-basics)/$",
        learn.views.web_app_tutorials_template),
    url("(?P<tutorial>adding-HTML-and-links-to-charts)/$",
        learn.views.web_app_tutorials_template)
)
