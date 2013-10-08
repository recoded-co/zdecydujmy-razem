__author__ = 'marcinra'
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns('django.contrib.auth.views',
url(r'^passreset/$','password_reset',{'template_name': 'registrations/password_reset_form.html'},name='forgot_password1'),
url(r'^passresetdone/$','password_reset_done',{'template_name': 'registrations/password_reset_done.html'},name='forgot_password2'),#),
url(r'^passresetconfirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$','password_reset_confirm',{'template_name': 'registrations/password_reset_confirm.html'},name='forgot_password3'),
url(r'^passresetcomplete/$','password_reset_complete',{'template_name': 'registrations/password_reset_complete.html'},name='forgot_password4'),
)