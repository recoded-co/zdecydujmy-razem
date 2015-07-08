__author__ = 'piotr'
from social_auth.middleware import SocialAuthExceptionMiddleware
from social_auth.exceptions import AuthCanceled
from django.http import HttpResponseRedirect

class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
	def process_exception(self, request, exception):
		if type(exception) == AuthCanceled:
			return HttpResponseRedirect("/")
		else:
			pass