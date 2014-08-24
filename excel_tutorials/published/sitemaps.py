import os

from django.conf import settings


def items():
    items = [
        dict(
            location='/how-to-make-a-box-plot-with-excel/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'excel_tutorials/',
                'how-to-make-a-box-plot-with-excel',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-bubble-chart-with-excel/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'excel_tutorials/',
                'how-to-make-a-bubble-chart-with-excel',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-graph-with-error-bars-with-excel/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'excel_tutorials/',
                'how-to-make-a-graph-with-error-bars-with-excel',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-graph-with-multiple-axes-with-excel/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'excel_tutorials/',
                'how-to-make-a-graph-with-multiple-axes-with-excel',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-line-graph-and-scatter-plot-with-excel/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'excel_tutorials/',
                'how-to-make-a-line-graph-and-scatter-plot-with-excel',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-heatmap-with-excel/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'excel_tutorials/',
                'how-to-make-a-heatmap-with-excel',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-histogram-with-excel/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'excel_tutorials/',
                'how-to-make-a-histogram-with-excel',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-bar-charts-with-excel/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'excel_tutorials/',
                'how-to-make-a-bar-charts-with-excel',
                'body.html'),
            priority=0.5
        )
    ]
    return items
