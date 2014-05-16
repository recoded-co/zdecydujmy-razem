# -*- coding: utf-8 -*-
# Example file, change according to your settings
from base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'm1-softgis',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'wertykulator',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl'
SITE_ID = 1

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7h4jc)!))$pu9)!y@3ny!d&amp;(s%gni3rjsc7($+s1heimp2-gp^'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/Users/dwa/src/gxmaps/gxmaps_app/GXENV/lib/python2.7/site-packages/django/contrib/gis/templates/",
)

#GOOGLE_API
GOOGLE_OAUTH2_CLIENT_ID = '459051988027-18drpshcid02rj3k92305fff0bhrcv7m.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'pl1ds5s6CiNqXLc_t1-P8M-a'
#GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile']
#GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True

#FACEBOOK_API
FACEBOOK_APP_ID              = '197797230425258'
FACEBOOK_API_SECRET          = '408d740771c205d0add77f24d46203b5'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# email configuration
EMAIL_HOST = 'mail.recoded.co'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'notification@recoded.co'
EMAIL_HOST_PASSWORD = '93WibOoo'
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'Zdecydujmyrazem <notification@recoded.co>'
NOTIFICATION_QUEUE_ALL = True