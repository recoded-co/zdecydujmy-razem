from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from zr.views import HomePageView, DashboardView, UserCreationPageView, SubscriptionList, SubscriptionDelete
from zr.api import router
from zr.api import RateListView, PostsListView

urlpatterns = patterns('gxmaps.views',
    #url(r'^test', TestView.as_view(), name="home"),
    url(r'^dashboard', DashboardView.as_view(), name="home"),
    url(r'^usercreate$', UserCreationPageView.as_view(), name="register"),
    # api
    url(r'^api/ratefilter', RateListView.as_view()),
    url(r'^api/postfilter', PostsListView.as_view()),
    url(r'^api/', include(router.urls), name="api_root"),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # subscriptions
    url(r'^settings/subscription/(?P<id>\d+)/delete/', SubscriptionDelete.as_view(), name="subscriptions_delete"),
    url(r'^settings/subscriptions', SubscriptionList.as_view(), name="subscriptions_list"),
    url(r'^api/postfilter', PostsListView.as_view()),

    url(r'^$', HomePageView.as_view(), name="home"),
)
