from rest_framework import viewsets, routers
from rest_framework.serializers import ModelSerializer
from rest_framework import filters
from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from filemanager.models import PostFileUpload
from zr.models import Plan, Configuration, Geometry, Subjects, Post, Rate, PostSubscription
from django_decorators.decorators import json_response
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()


class PlanViewSet(viewsets.ModelViewSet):
    model = Plan

router.register(r'plans', PlanViewSet)


class ConfigurationViewSet(viewsets.ModelViewSet):
    model = Configuration

router.register(r'configurations', ConfigurationViewSet)


class GeometrySerializer(ModelSerializer):
    geoelement = serializers.Field(source='geoElement')

    class Meta:
        model = Geometry
        fields = ('id', 'name', 'geoelement', 'poly', 'point')


class GeometryViewSet(viewsets.ModelViewSet):
    queryset = Geometry.objects.all()
    serializer_class = GeometrySerializer

    def pre_save(self, obj):
        print 'pre_save %s' % str(obj)

    def post_save(self, obj, created=False):
        print 'post save %s' % str(obj)

    def pre_delete(self, obj):
        print 'pre delete %s' % str(obj)

    def post_delete(self, obj):
        print 'post delete %s' % str(obj)

router.register(r'geometries', GeometryViewSet)


class SubjectsViewSet(viewsets.ModelViewSet):
    model = Subjects

router.register(r'subjects', SubjectsViewSet)


class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate

class FileSerializer(ModelSerializer):
    class Meta:
        model = PostFileUpload

class PostSerializer(ModelSerializer):
    rate = serializers.Field(source='has_rate')
    score = serializers.Field(source='has_likes')
    author_name = serializers.Field(source='author_name')
    filep =  FileSerializer(required=False,many=True)
    positive_rate = serializers.Field(source='like_sum')
    negative_rate = serializers.Field(source='dislike_sum')

    class Meta:
        model = Post
        fields = ('id','author', 'author_name',
                  'parent', 'plan', 'content',
                  'rate', 'score','geometry',
                  'date','filep','positive_rate','negative_rate')

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        queryset = Post.objects.all() # TODO add plan parameter!!
        serializer = PostSerializer(queryset, many=True)
        result = []
        # TODO make this in one query

        if str(request.user) != "AnonymousUser" :
            subscribed_posts = [p.post.id for p in PostSubscription().get_user_subscriptions(request.user)]
        else:
            subscribed_posts = []
        for entry in serializer.data:
            if entry['id'] in subscribed_posts:
                entry['subscription'] = True
            else:
                entry['subscription'] = False
            result.append(entry)

        if str(request.user) != "AnonymousUser" :
            subscribed_rates = [p.post.id for p in Rate().get_user_like(request.user)]
        else:
            subscribed_rates = []
        for entry in serializer.data:
            if entry['id'] in subscribed_rates:
                entry['sub_rates'] = True
            else:
                entry['sub_rates'] = False
            result.append(entry)

        return Response(result)

router.register(r'posts', PostViewSet)


class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateListView(generics.ListAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = (filters.DjangoFilterBackend,)

router.register(r'rates', RateViewSet)


class PostsListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_fields = ('id', 'author')


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = PostSubscription


class PostSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = PostSubscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return PostSubscription.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        import json
        data = json.loads(request.raw_post_data)
        post = Post.objects.get(id=data['post'])
        subscription, created = PostSubscription.objects.get_or_create(user=request.user, post=post)
        self.subscription = subscription
        return super(PostSubscriptionViewSet, self).update(request, args, kwargs)

    def get_object_or_none(self ):
        return self.subscription

router.register(r'subscriptions', PostSubscriptionViewSet)


#@csrf_exempt
@json_response
def geo_search(request, plan_id):
    from django.db.models import Q
    from django.contrib.gis.geos import fromstr
    from django.http import HttpResponseBadRequest
    import json
    polygon = request.POST.get('wkt', None)
    if polygon:
        print polygon
        try:
            pnt = fromstr(polygon, srid=4326)
            print pnt
            geometries = Geometry.objects.filter(Q(poly__intersects=pnt) | Q(point__intersects=pnt))
            posts = Post.objects.filter(plan__id=plan_id, geometry__in=geometries)
            print geometries
            print posts
            posts_serialized = PostSerializer(posts, many=True)
            print posts_serialized.data
            #json_geometries = GeometrySerializer(geometries, many=True)
            #print json_geometries.data
            return posts_serialized.data #json_geometries.data
        except Exception, e:
            return json.dumps({'result': 'exception'})
    else:
        return HttpResponseBadRequest(json.dumps({'result': 'error'}))




"""
within
Availability: PostGIS, Oracle, MySQL, SpatiaLite

Tests if the geometry field is spatially within the lookup geometry.

Example:

Zipcode.objects.filter(poly__within=geom)
"""