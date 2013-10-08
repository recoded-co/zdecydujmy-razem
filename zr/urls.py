from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from zr.views import HomePageView, DashboardView, UserCreationPageView
from zr.api import router

urlpatterns = patterns('gxmaps.views',
    url(r'^dashboard', DashboardView.as_view(), name="home"),
    url(r'^usercreate$', UserCreationPageView.as_view(), name="register"),
    # api
    url(r'^api/', include(router.urls), name="api_root"),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^$', HomePageView.as_view(), name="home"),
)
