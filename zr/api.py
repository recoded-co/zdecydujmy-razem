from rest_framework import viewsets, routers
from rest_framework.serializers import ModelSerializer
from rest_framework import filters
from rest_framework import generics
from rest_framework import serializers
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.renderers import JSONRenderer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from filemanager.models import PostFileUpload
from zr.models import Plan, Configuration, Geometry, Post, Rate, PostSubscription, TrackEvents
from zr.models import Subject, SubjectFeat, SubjectFeatProperty
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
    geo_id = serializers.Field(source='geoId')

    class Meta:
        model = Geometry
        fields = ('id', 'name', 'geoelement', 'geo_id', 'poly', 'point')


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
    filep =  FileSerializer(required=False, many=True)
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
        # TODO do it right!
        if str(request.user) != "AnonymousUser":
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


class SubscriptionList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    queryset = PostSubscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return PostSubscription.objects.filter(user=self.request.user)
        else:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied('You can only subscribe for yourself')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        from django.core.exceptions import PermissionDenied
        user_id = int(request.DATA['user'])
        post_id = int(request.DATA['post'])
        if request.user.is_authenticated() and user_id == request.user.id:
            try:
                subscriptions = PostSubscription.objects.filter(user=request.user, post__id=post_id)
                for s in subscriptions:
                    s.delete()
            except PostSubscription.DoesNotExist:
                pass
            return self.create(request, args, kwargs)
        else:
            raise PermissionDenied('You have to be logged in and you can only subscribe for yourself')

class SubscriptionDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    queryset = PostSubscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        user_id = int(request.DATA['user'])
        if request.user.id == user_id:
            return self.update(request, *args, **kwargs)
        else:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied('You can edit only yours subscription')

    def delete(self, request, *args, **kwargs):
        user_id = int(request.DATA['user'])
        if request.user.id == user_id:
            return self.destroy(request, *args, **kwargs)
        else:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied('You can remove only yours subscriptions')

"""

class PostSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = PostSubscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        from django.core.exceptions import PermissionDenied
        if self.request.user.is_authenticated():
            return PostSubscription.objects.filter(user=self.request.user)
        else:
            raise PermissionDenied('You can only subscribe for yourself')

    def create(self, request, *args, **kwargs):
        user_id = int(request.DATA['user'])
        print '%s vs %s' % (user_id, request.user.id)
        if user_id != request.user.id:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied('You can only subscribe for yourself')

        post_id = int(request.DATA['post'])
        if PostSubscription.objects.filter(user__id=user_id, post__id=post_id).exists():
            return super(PostSubscriptionViewSet, self).update(request, args, kwargs)
        else:
            return super(PostSubscriptionViewSet, self).create(request, args, kwargs)
"""

#router.register(r'subscriptions', PostSubscriptionViewSet)


class TrackEventsSerializer(ModelSerializer):
    class Meta:
        model = TrackEvents


class TrackEventsViewSet(viewsets.ModelViewSet):
    queryset = TrackEvents.objects.all()
    serializer_class = TrackEventsSerializer

    def get_queryset(self):
        return TrackEvents.objects.all()

    def list(self, request):
        queryset = TrackEvents.objects.all()
        serializer = TrackEventsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        import json
        data = json.loads(request.raw_post_data)
        labels = ['category','action','opt_label','opt_value','opt_noninteraction']
        inputs = {}
        for item in labels:
            if item in data:
                inputs[item]=data[item]
            else:
                inputs[item]=''
        trackevent = TrackEvents.objects.create(**inputs)
        self.trackevent = trackevent
        return super(TrackEventsViewSet, self).update(request, args, kwargs)

    def get_object_or_none(self, request, *args, **kwargs):
        return self.trackevent

router.register(r'track', TrackEventsViewSet)


#@csrf_exempt
@json_response
def geo_search(request, plan_id):
    from django.db.models import Q
    from django.contrib.gis.geos import fromstr
    from django.http import HttpResponseBadRequest
    import json
    polygon = request.POST.get('wkt', None)
    if polygon:
        #print polygon
        try:
            pnt = fromstr(polygon, srid=4326)
            geometries = Geometry.objects.filter(Q(poly__intersects=pnt) | Q(point__intersects=pnt))
            posts = Post.objects.filter(plan__id=plan_id, geometry__in=geometries)
            posts_serialized = PostSerializer(posts, many=True)
            return posts_serialized.data #json_geometries.data
        except Exception, e:
            return json.dumps({'result': 'exception'})
    else:
        return HttpResponseBadRequest(json.dumps({'result': 'error'}))


class SubjectFeatPropertySerializer(ModelSerializer):
    class Meta:
        model = SubjectFeatProperty
        fields = ('key', 'value')

class SubjectFeatSerializer(GeoFeatureModelSerializer):
    feat_description = SubjectFeatPropertySerializer(many=True) #serializers.RelatedField(many=True)

    class Meta:
        model = SubjectFeat
        geo_field = "geom"
        fields = ('id', 'subject', 'geom', 'feat_description')

class SubjectFeatList(generics.ListAPIView):
    queryset = SubjectFeat.objects.all()
    serializer_class = SubjectFeatSerializer

