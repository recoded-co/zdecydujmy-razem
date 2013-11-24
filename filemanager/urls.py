from django.conf.urls import patterns, url, include
from filemanager.views import FileManager, angular_post

urlpatterns = patterns('',
    url(r'^/(?P<file_id>.+)$',FileManager.as_view()),
    url(r'^$', FileManager.as_view(), name="fm"),
    url(r'angular_post^$','filemanager.views.angular_post' ),
)
