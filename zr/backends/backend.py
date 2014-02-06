__author__ = 'marcinra'

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class LowercaseAuthenticationBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

class EmailAuthenticationBackend(ModelBackend):
    """
    Authenticate against django.contrib.auth.models.User using
    e-mail address instead of username.
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None