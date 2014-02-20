from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from zr.views import HomePageView, DashboardView, UserCreationPageView, SubscriptionList, SubscriptionDelete
from zr.views import ZipcodeCheckView
from zr.api import router
from zr.api import RateListView, PostsListView, geo_search, BasePlanJson

urlpatterns = patterns('',
    #url(r'^test', TestView.as_view(), name="home"),
    url(r'^dashboard', DashboardView.as_view(), name="dashboard"),
    url(r'^usercreate$', UserCreationPageView.as_view(), name="register"),
    # api
    url(r'^api/ratefilter', RateListView.as_view()),
    url(r'^api/postfilter', PostsListView.as_view()),
    url(r'^api/geosearch/(?P<plan_id>\d+)/?', geo_search, name='geo_search'),
    url(r'^api/subjects/(?P<plan_id>\d+)/?$', BasePlanJson.as_view(), name='subjects_geojson'),
    url(r'^api/', include(router.urls), name="api_root"),

    url(r'^fmen/', include('filemanager.urls')),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # subscriptions
    url(r'^settings/subscription/(?P<id>\d+)/delete/', SubscriptionDelete.as_view(), name="subscriptions_delete"),
    url(r'^settings/subscriptions', SubscriptionList.as_view(), name="subscriptions_list"),
    url(r'^settings/zipcode_check', ZipcodeCheckView.as_view(), name='zipcode_check'),
    url(r'^api/postfilter', PostsListView.as_view()),

    url(r'^$', HomePageView.as_view(), name="home"),
)
