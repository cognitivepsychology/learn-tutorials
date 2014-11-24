import os

from django.conf import settings


def items():
    items = [
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
            location='/how-to-make-a-line-graph-and-scatter-plot-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-line-graph-and-scatter-plot-online',
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
            location='/how-to-make-an-area-chart-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-an-area-chart-online',
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
            location='/how-to-make-a-heatmap-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-heatmap-online',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-graph-with-error-bars-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-graph-with-error-bars-online',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-graph-with-multiple-axes-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-graph-with-multiple-axes-online',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-sign-up-to-plotly/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-sign-up-to-plotly',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-embed-plotly-graphs-in-websites/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-embed-plotly-graphs-in-websites',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-share-and-print-plotly-graphs/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-share-and-print-plotly-graphs',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-3d-line-chart-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-3d-line-chart-online',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/how-to-make-a-3d-scatter-plot-online/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'how-to-make-a-3d-scatter-plot-online',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/date-format-and-time-series/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'date-format-and-time-series',
                'body.html'),
            priority=0.5
        ),
        dict(
            location='/LaTeX-basics/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'web_app_tutorials',
                'LaTeX-basics',
                'body.html'),
            priority=0.5
        )
    ]
    return items
