from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from zr.views import HomePageView, DashboardView, UserCreationPageView #, TestView
from zr.api import router
from zr.api import RateListView, PostsListView

urlpatterns = patterns('',
    #url(r'^test', TestView.as_view(), name="home"),
    url(r'^dashboard', DashboardView.as_view(), name="dashboard"),
    url(r'^usercreate$', UserCreationPageView.as_view(), name="register"),
    # api
    url(r'^api/ratefilter', RateListView.as_view()),
    url(r'^api/postfilter', PostsListView.as_view()),
    url(r'^api/', include(router.urls), name="api_root"),
    url(r'^fmen/', include('filemanager.urls')),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^$', HomePageView.as_view(), name="home"),
)
