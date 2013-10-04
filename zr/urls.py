from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from zr.views import HomePageView, DashboardView, UserCreationPageView

urlpatterns = patterns('gxmaps.views',
    url(r'^dashboard', DashboardView.as_view(), name="home"),
    url(r'^usercreate$', UserCreationPageView.as_view(), name="register"),
    url(r'^$', HomePageView.as_view(), name="home"),

)
