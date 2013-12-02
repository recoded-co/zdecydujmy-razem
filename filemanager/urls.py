from django.conf.urls import patterns, url, include
from filemanager.views import FileManager, angular_post
from zdecydujmyrazem import settings

urlpatterns = patterns('',
    #url(r'^(?P<file_id>.+)$',FileManager.as_view()),
    url(r'^download/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^angular_post$','filemanager.views.angular_post' ),
    url(r'^$', FileManager.as_view(), name="fm"),

)
