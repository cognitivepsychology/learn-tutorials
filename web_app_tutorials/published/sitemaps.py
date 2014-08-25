import os

from django.conf import settings


def items():
    items = [
        dict(
            location='/how-to-make-a-bubble-chart-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-bubble-chart-online',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/area-chart-tutorial/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'area-chart-tutorial',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/multiple-axes-tutorial/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'multiple-axes-tutorial',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-line-graph-and-scatter-plot/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-line-graph-and-scatter-plot',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/add-data-to-the-plotly-grid/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'add-data-to-the-plotly-grid',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-graph-with-error-bars/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-graph-with-error-bars',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-bar-chart-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-bar-chart-online',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-histogram-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-histogram-online',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-box-plot-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-box-plot-online',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-heatmap-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-heatmap-online',
                'body.html'),
            priority=0.5
        )
    ]
    return items
