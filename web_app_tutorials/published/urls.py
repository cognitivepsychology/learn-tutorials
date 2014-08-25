from django.conf.urls import patterns, url

import learn.views


urlpatterns = patterns(
    '',
    url("(?P<tutorial>how-to-make-a-bubble-chart-online)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>area-chart-tutorial)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>multiple-axes-tutorial)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-line-graph-and-scatter-plot)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>add-data-to-the-plotly-grid)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-graph-with-error-bars)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-bar-chart-online)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-histogram-online)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-box-plot-online)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-heatmap-online)/$",
        learn.views.excel_tutorials_template)
)
