from django.conf.urls import patterns, url

import learn.views

urlpatterns = patterns(
   '',
    url("(?P<excel_tutorial>box-plots-in-excel-with-plotly)/$", learn.views.excel_tutorials_template),
    url("(?P<excel_tutorial>bubble-charts-in-excel-with-plotly)/$", learn.views.excel_tutorials_template),
    url("(?P<excel_tutorial>error-bars-in-excel-with-plotly)/$", learn.views.excel_tutorials_template),
    url("(?P<excel_tutorial>multiple-axes-plots-in-excel-with-plotly)/$", learn.views.excel_tutorials_template),
    url("(?P<excel_tutorial>scatter-and-line-plots-in-excel-with-plotly)/$", learn.views.excel_tutorials_template),
    url("(?P<excel_tutorial>heatmaps-in-excel-with-plotly)/$", learn.views.excel_tutorials_template),
    url("(?P<excel_tutorial>histograms-in-excel-with-plotly)/$", learn.views.excel_tutorials_template),
    url("(?P<excel_tutorial>bar-charts-in-excel-with-plotly)/$", learn.views.excel_tutorials_template)
)
