from django.conf.urls import patterns, url

import learn.views


urlpatterns = patterns(
    '',
    url("(?P<tutorial>how-to-make-a-bar-chart-with-excel)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-box-plot-with-excel)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-bubble-chart-with-excel)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-graph-with-error-bars-with-excel)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-heatmap-with-excel)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-histogram-with-excel)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-line-graph-and-scatter-plot-with-excel)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-a-graph-with-multiple-axes-with-excel)/$",
        learn.views.excel_tutorials_template),
    url("(?P<tutorial>how-to-make-an-area-chart-with-excel)/$",
        learn.views.excel_tutorials_template)
)
