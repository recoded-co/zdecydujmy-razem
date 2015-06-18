"""
Django settings for zdecydujmyrazem project.
"""
import os
from datetime import date


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = ''

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['127.0.0.1',]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # 3rd party apps
    'notification',
    'bootstrap_toolkit',
    'floppyforms',
    'rest_framework',
    'social_auth',
    'registration',

    # project apps
    'zr',
    'filemanager',
    'avatar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    )

ROOT_URLCONF = 'zdecydujmyrazem.urls'

WSGI_APPLICATION = 'zdecydujmyrazem.wsgi.application'

DATABASES = {}

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

LOGIN_URL = '/social_auth/login/'

LOGIN_ERROR_URL = '/social_auth/login-error/'

LOGIN_REDIRECT_URL = '/zr/settings/zipcode_check'

HOME_PAGE_URL = '/zr/dashboard'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'zr.backends.backend.LowercaseAuthenticationBackend',
    'zr.backends.backend.EmailAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AVATAR_AUTO_GENERATE_SIZES = (20,40,80,174,)

AVATAR_STORAGE_DIR = 'avatar/'

AVATAR_GRAVATAR_BACKUP = False

AVATAR_DEFAULT_URL = '/images/ap_maj6_wymiary-10.png'

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

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.user.update_user_details',
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('google', 'facebook')

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

INDEX_LAST_UPDATE = date.min

AUTH_PROFILE_MODULE = 'zr.Profile'

try:
    execfile(os.path.join(os.path.dirname(__file__), 'local.py'))
except IOError:
    pass
