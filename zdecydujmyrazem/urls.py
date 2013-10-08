from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',

    url(r'^zr/', include('zr.urls')),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'zr/index.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^accounts/', include('registrations.urls')),
    url(r'^social_auth/', include('social_auth.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^.*$', RedirectView.as_view(url='/zr/'), name='go_home'),
)

