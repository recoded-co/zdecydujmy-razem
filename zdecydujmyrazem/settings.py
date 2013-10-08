# -*- coding: utf-8 -*-
# Example file, change according to your settings
from base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dbname',                      # Or path to database file if using sqlite3.
        'USER': 'dbuser',                      # Not used with sqlite3.
        'PASSWORD': 'dbpass',                  # Not used with sqlite3.
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
)

#GOOGLE_API
GOOGLE_OAUTH2_CLIENT_ID      = '302320688030.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET  = '8t62189JvWZhZs7cm6snrpAd'
#GOOGLE_OAUTH_EXTRA_SCOPE = ['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile']
#GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True

#FACEBOOK_API
FACEBOOK_APP_ID              = '623947990960027'
FACEBOOK_API_SECRET          = '6744498d9d894e1f0b8b1d6fff65cf1e'

#TODO: skonfigurować server pocztowy.
EMAIL_HOST = ''#'smtp.gmail.com'
EMAIL_PORT = 0#465
EMAIL_USE_TLS = True

EMAIL_HOST_USER = ''#'my@gmail.com'
EMAIL_HOST_PASSWORD = ''#'my_emails_password'