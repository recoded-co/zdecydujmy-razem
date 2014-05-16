# Recoded additional settings
LOGIN_REDIRECT_URL = '/zr/settings/zipcode_check'
HOME_PAGE_URL = '/zr/dashboard'
from datetime import date
INDEX_LAST_UPDATE = date.min

AUTH_PROFILE_MODULE = 'zr.Profile'

# Django settings for zdecydujmyrazem project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',                # LNZ
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',            # LNZ
    'geonition_utils.middleware.PreventCacheMiddleware',    # LNZ
    'geonition_utils.middleware.IEEdgeMiddleware',          # LNZ
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.debug",                 # LNZ
    "django.core.context_processors.i18n",                  # LNZ
    "django.core.context_processors.media",                 # LNZ
    "django.core.context_processors.static",                # LNZ
    "django.core.context_processors.tz",                    # LNZ
    "django.contrib.messages.context_processors.messages",  # LNZ
    "django.core.context_processors.request",               # LNZ
    "base_page.context_processors.organization"             # LNZ
    'social_auth.context_processors.social_auth_by_type_backends',
)

ROOT_URLCONF = 'zdecydujmyrazem.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'zdecydujmyrazem.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    # Uncomment the next line to enable the admin:
    'django.contrib.admin',

    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    # Recoded - additional modules
    'notification',
    'bootstrap_toolkit',
    'floppyforms',
    'rest_framework',
    'social_auth',
    'registration',
    #'django_extensions',
    # Made by Recoded:
    'zr',
    'filemanager',
    'avatar',

)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.user.update_user_details',
    #'social_auth.backends.pipeline.misc.save_status_to_session',
    #'zr.auth_pipeline.get_user_zipcode',
    #'zr.auth_pipeline.store_user_zipcode',

)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'zr.backends.backend.LowercaseAuthenticationBackend',
    'zr.backends.backend.EmailAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)


SOCIAL_AUTH_ENABLED_BACKENDS = ('google', 'facebook')

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
#SOCIAL_AUTH_UID_LENGTH = 32 # default 255
#SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 32 # default 255
#SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 32  # default 255
#SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 32 # default 255
#SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 32 # default 255

LOGIN_URL          = '/social_auth/login/'
#LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/social_auth/login-error/'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# email configuration
EMAIL_HOST = 'mail.recoded.co'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'notification@recoded.co'
EMAIL_HOST_PASSWORD = '93WibOoo'
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'ZdecydujmyRazem <notification@recoded.co>'
NOTIFICATION_QUEUE_ALL = True

#Avatar

#AUTO_GENERATE_AVATAR_SIZES = (20,40,80,)
AVATAR_AUTO_GENERATE_SIZES = (20,40,80,)

#The method to use when resizing images, based on the options available in PIL. Defaults to Image.ANTIALIAS.
#AVATAR_RESIZE_METHOD

#The directory under MEDIA_ROOT to store the images. If using a non-filesystem storage device, this will simply be appended to the beginning of the file name.
AVATAR_STORAGE_DIR = 'avatar/'

#    A boolean determining whether to default to the Gravatar service if no Avatar instance is found in the system for the given user. Defaults to True.
AVATAR_GRAVATAR_BACKUP = True

#   The default URL to default to if AVATAR_GRAVATAR_BACKUP is set to False and there is no Avatar instance found in the system for the given user.
AVATAR_DEFAULT_URL = '/images/anonymous.jpg'
