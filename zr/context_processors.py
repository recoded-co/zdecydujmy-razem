__author__ = 'darek'
from django.conf import settings


def analytics_settings(request):
    return {
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
    }