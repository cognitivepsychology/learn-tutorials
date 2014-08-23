import os

from django.conf import settings

def items():
    items = [
        dict(
            location='/box-plots-in-excel-with-plotly/',
            lmfile=os.path.join(settings.TOP_DIR,'shelly','templates','learn','includes','excel_tutorials','box-plots-in-excel-with-plotly','body.html'),
            priority=0.5
        ),
        dict(
            location='/bubble-charts-in-excel-with-plotly/',
            lmfile=os.path.join(settings.TOP_DIR,'shelly','templates','learn','includes','excel_tutorials','bubble-charts-in-excel-with-plotly','body.html'),
            priority=0.5
        ),
        dict(
            location='/error-bars-in-excel-with-plotly/',
            lmfile=os.path.join(settings.TOP_DIR,'shelly','templates','learn','includes','excel_tutorials','error-bars-in-excel-with-plotly','body.html'),
            priority=0.5
        ),
        dict(
            location='/multiple-axes-plots-in-excel-with-plotly/',
            lmfile=os.path.join(settings.TOP_DIR,'shelly','templates','learn','includes','excel_tutorials','multiple-axes-plots-in-excel-with-plotly','body.html'),
            priority=0.5
        ),
        dict(
            location='/scatter-and-line-plots-in-excel-with-plotly/',
            lmfile=os.path.join(settings.TOP_DIR,'shelly','templates','learn','includes','excel_tutorials','scatter-and-line-plots-in-excel-with-plotly','body.html'),
            priority=0.5
        ),
        dict(
            location='/heatmaps-in-excel-with-plotly/',
            lmfile=os.path.join(settings.TOP_DIR,'shelly','templates','learn','includes','excel_tutorials','heatmaps-in-excel-with-plotly','body.html'),
            priority=0.5
        ),
        dict(
            location='/histograms-in-excel-with-plotly/',
            lmfile=os.path.join(settings.TOP_DIR,'shelly','templates','learn','includes','excel_tutorials','histograms-in-excel-with-plotly','body.html'),
            priority=0.5
        ),
        dict(
            location='/bar-charts-in-excel-with-plotly/',
            lmfile=os.path.join(settings.TOP_DIR,'shelly','templates','learn','includes','excel_tutorials','bar-charts-in-excel-with-plotly','body.html'),
            priority=0.5
        )
    ]
    return items
