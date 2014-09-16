import os

from django.conf import settings


def items():
    items = [
        dict(
            location='/basic-statistics-tutorial/',
            lmfile=os.path.join(
                settings.TOP_DIR, 'shelly',
                'templates', 'learn', 'includes',
                'data_literacy',
                'basic-statistics-tutorial',
                'body.html'),
            priority=0.5
        )
    ]
    return items
