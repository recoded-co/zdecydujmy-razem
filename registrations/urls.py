from django.conf.urls import patterns, url

__author__ = 'marcinra'

urlpatterns = patterns('',
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'registrations/password_reset_form.html'},
        name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done',
        {'template_name': 'registrations/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'registrations/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'registrations/password_reset_complete.html'},
        name='password_reset_complete'),
)
