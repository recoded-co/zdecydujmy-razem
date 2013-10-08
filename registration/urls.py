__author__ = 'marcinra'
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
url(r'^passreset/$',auth_views.password_reset,name='forgot_password1'),
url(r'^passresetdone/$',auth_views.password_reset_done,name='forgot_password2'),
url(r'^passresetconfirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,name='forgot_password3'),
url(r'^passresetcomplete/$',auth_views.password_reset_complete,name='forgot_password4'),
)