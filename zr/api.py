# -*- coding: utf-8 -*-
from rest_framework import viewsets, routers
from rest_framework.serializers import ModelSerializer
from rest_framework import filters, status
from rest_framework import generics
from rest_framework import serializers
from rest_framework import mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from filemanager.models import PostFileUpload
from zr.models import Plan, Configuration, Geometry, Post, Rate, PostSubscription, TrackEvents
from zr.models import Subject, SubjectFeat, SubjectFeatProperty
from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt
from avatar.util import get_default_avatar_url
from avatar.templatetags.avatar_tags import avatar_url
from django.utils import six
from django.db import connection
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User
import datetime


router = routers.DefaultRouter()


class PlanViewSet(viewsets.ModelViewSet):
    model = Plan
    queryset = Plan.objects.all()

router.register(r'plans', PlanViewSet)


class ConfigurationViewSet(viewsets.ModelViewSet):
    model = Configuration
    queryset = Configuration.objects.all()

router.register(r'configurations', ConfigurationViewSet)


class GeometrySerializer(ModelSerializer):
    geoelement = serializers.CharField(source='geoElement', required=False)
    geo_id = serializers.CharField(source='geoId', required=False)

    class Meta:
        model = Geometry
        fields = ('id', 'name', 'geoelement', 'geo_id', 'poly', 'point', 'line')


class GeometryViewSet(viewsets.ModelViewSet):
    queryset = Geometry.objects.all()
    serializer_class = GeometrySerializer


router.register(r'geometries', GeometryViewSet)


class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate


class FileSerializer(ModelSerializer):
    class Meta:
        model = PostFileUpload


class PostSerializer(ModelSerializer):
    rate = serializers.IntegerField(source='has_rate', required=False)
    score = serializers.IntegerField(source='has_likes', required=False)
    author_name = serializers.CharField(required=False)
    content = serializers.SerializerMethodField()
    filep =  FileSerializer(required=False, many=True)
    positive_rate = serializers.IntegerField(source='like_sum', required=False)
    negative_rate = serializers.IntegerField(source='dislike_sum', required=False)
    author_is_staff = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author', 'author_name', 'author_is_staff',
                  'parent', 'plan', 'content',
                  'rate', 'score', 'geometry',
                  'date', 'filep', 'positive_rate','negative_rate', 'is_removed',
                  'is_subscribed', 'is_owned',
        )

    def get_content(self, obj):
        if obj.is_removed:
            return u"Komentarz usunięty przez administratora."
        else:
            return obj.content

    def get_author_is_staff(self, obj):
        if obj.author.is_staff:
            return True

        return False

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user and not request.user.is_anonymous():
            return obj.postsubscription_set.filter(user=request.user, active=True).exists()

        return False
    def get_is_owned(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user == obj.author:
            return True

        return False

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        queryset = Post.objects.all() # TODO add plan parameter!!
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        result = []
        # TODO make this in one query
        # TODO do it right!
        if str(request.user) != "AnonymousUser":
            subscribed_posts = [p.post.id for p in PostSubscription().get_user_subscriptions(request.user)]
        else:
            subscribed_posts = []

        for entry in serializer.data:
            user = User.objects.get(username=entry['author_name'])
            alt = six.text_type(user)
            url = avatar_url(user, 40)
            entry['avatar_url']=url
            entry['avatar_alt']=alt

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        instance = serializer.instance

        instance.content = request.data['content']
        instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @list_route(methods=['post'])
    def remove(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'message': u'Brak uprawnień by wykonać tę akcję.'},
                status=status.HTTP_400_BAD_REQUEST
            )


        id = request.data.get('id')
        if id:
            try:
                post = Post.objects.get(pk=id)
                post.is_removed = True
                post.save()
                return Response({'message': 'Usunięto wpis.'})

            except Post.DoesNotExist:
                return Response(
                    {'message': 'Nie odnaleziono wpisu.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {'message': 'Brak ID.'},
            status=status.HTTP_400_BAD_REQUEST
        )

router.register(r'posts', PostViewSet)


class NSubscribed(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):

        post_subscription_list = []
        if self.request.user.is_authenticated():
            post_subscription_list = PostSubscription.objects.filter(user=self.request.user, active=True)
            if len(post_subscription_list)==0:
                return Response([])
        else:
            return Response([])

        type = request.QUERY_PARAMS.get('type','date')
        direction = self.parseToBoolean(request.QUERY_PARAMS.get('direction',True))
        round = int(request.QUERY_PARAMS.get('round',1))
        plan_id = request.QUERY_PARAMS.get('plan_id','None')
        parent = request.QUERY_PARAMS.get('parent','None')

        cursor = connection.cursor()
        sql = 'SELECT id ,  \
               (select count(*) from zr_post where parent_id = a.id) as numcom, \
               geometry_id \
               FROM zr_post as a '

        parent_sql = ''
        params = []

        if plan_id == 'None':
            sql += 'where plan_id is null '
        elif int(float(plan_id))>=0:
            sql += 'where plan_id = ' + str(int(float(plan_id)))

        if len(post_subscription_list) > 0 and parent == 'None':
            sql += ' and id in (%s)' % (','.join([unicode(i.post.id) for i in post_subscription_list]))

        elif parent != 'None':
            sql += 'and parent_id = %s '
            params.append(parent)

        order_by_sql = ' '
        if type == 'date' :
            if direction :
                sql += 'order by date desc '
            else :
                sql += 'order by date '
        elif type == 'com':
            if direction :
                sql += 'order by numcom desc '
            else :
                sql += 'order by numcom '

        cursor.execute(sql, params)
        row = cursor.fetchall()
        paginator = Paginator(row, 25);

        try:
            actuall_item_list = paginator.page(round).object_list
        except EmptyPage:
            return Response([])

        temp_ret = []

        for item in actuall_item_list:
            temp = Post.objects.get(pk = item[0] )
            temp_data = PostSerializer(temp, context={'request': request})
            user = User.objects.get(username=temp_data.data['author_name'])
            alt = six.text_type(user)
            url = avatar_url(user, 40)
            temp_data.data['avatar_url']=url
            temp_data.data['avatar_alt']=alt
            temp_data.data['numcom'] = int(item[1])
            temp_ret.append(temp_data.data)

        return Response(temp_ret)

    def parseToBoolean(self, str):
        if str == 'True':
            return True
        else:
            return False


class NPost(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):

        parent = request.QUERY_PARAMS.get('parent','None')
        geometry = request.QUERY_PARAMS.get('geometry', 'None')
        type = request.QUERY_PARAMS.get('type','date')
        direction = NPost.parseToBoolean(request.QUERY_PARAMS.get('direction',True))
        round = int(request.QUERY_PARAMS.get('round',1))
        plan_id = request.QUERY_PARAMS.get('plan_id','None')
        LIMIT = 0
        #print "parent,geometry,type,direction,round"
        #print parent,geometry,type,direction,round

        cursor = connection.cursor()
        sql = 'SELECT id ,  \
               (select count(*) from zr_post where parent_id = a.id) as numcom, \
               geometry_id \
               FROM zr_post as a '

        parent_sql = ''
        params = []

        if parent != 'None':
            LIMIT=50
            sql += 'where parent_id = %s '
            params.append(parent)
        else :
            LIMIT=25
            sql += 'where parent_id is null '

        if plan_id == 'None':
            sql += ' and plan_id is null '
        elif int(float(plan_id))>=0:
            sql += ' and plan_id = %s '
            params.append(str(int(float(plan_id))))

        if geometry == 'None':
            sql += ' and geometry_id is null '
        elif geometry == 'notNone':
            sql += ' and geometry_id is not null '
        elif len(geometry.split(','))== 1 and int(float(geometry)) == -1:
            return Response([])
        elif len(geometry.split(',')) == 1:
            try:
                if int(geometry)>0:
                    sql += ' and geometry_id = ' + str(int(float(geometry))) + ' '
            except ValueError:
                print 'ValueError'
        elif len(geometry.split(','))>1:
            try:
                param_list = str(tuple([int(float(i)) for i in geometry.split(',')]))
                sql += ' and geometry_id in ' + param_list + ' '
                #print param_list
                #params.append(param_list)
            except ValueError:
                print 'ValueError'

        order_by_sql = ' '
        if type == 'date' :
            if direction :
                sql += 'order by date desc '
            else:
                sql += 'order by date '
        elif type == 'com':
            if direction :
                sql += 'order by numcom desc '
            else:
                sql += 'order by numcom '

        cursor.execute(sql, params)
        row = cursor.fetchall()
        paginator = Paginator(row,LIMIT);

        try:
            actuall_item_list = paginator.page(round).object_list
        except EmptyPage:
            return Response([])

        temp_ret = []

        temp_ret = NPost.addDataToOutput(actuall_item_list, request=request)


        return Response(temp_ret)

    @staticmethod
    def addDataToOutput(actuall_item_list, request=None):
        return_list =[]

        for item in actuall_item_list:
            post = Post.objects.get(pk = item[0] )
            post_serialized = PostSerializer(post, context={'request': request})

            data = post_serialized.data

            user = User.objects.get(username=data['author_name'])
            alt = six.text_type(user)
            url = avatar_url(user, 40)

            data['avatar_url']=url
            data['avatar_alt']=alt
            data['numcom'] = int(item[1])

            return_list.append(data)

        return return_list

    @staticmethod
    def parseToBoolean(str):
        if str == 'True':
            return True
        else :
            return False


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
        from rest_framework import status
        from rest_framework.response import Response
        data = request.DATA
        labels = ['category', 'action', 'opt_label', 'opt_value', 'opt_noninteraction']
        inputs = {}
        for item in labels:
            if item in data:
                inputs[item] = data[item]
            else:
                inputs[item] = ''
        inputs['opt_label'] = str(request.user)
        inputs['opt_noninteraction'] = request.session.session_key
        trackevent = TrackEvents.objects.create(**inputs)
        return Response(TrackEventsSerializer(trackevent).data, status=status.HTTP_201_CREATED)

router.register(r'track', TrackEventsViewSet)


#@csrf_exempt
@json_view
def geo_search(request, plan_id):
    from django.db.models import Q
    from django.contrib.gis.geos import fromstr

    polygon = request.POST.get('wkt', None)

    if polygon:
        try:
            pnt = fromstr(polygon, srid=4326)
            geometries = Geometry.objects.filter(Q(poly__intersects=pnt) | Q(point__intersects=pnt) | Q(line__intersects=pnt))
            posts = Post.objects.filter(plan__id=plan_id, geometry__in=geometries)
            posts_serialized = PostSerializer(posts, many=True)
            return posts_serialized.data
        except Exception, e:
            return {'result': 'exception'}, 500
    else:
        return {'result': 'error'}, 500


@json_view
def keyword_search(request, plan_id, query):

    parent = request.GET.get('parent', 'None')
    geometry = request.GET.get('geometry', 'None')
    type = request.GET.get('type', 'date')
    direction = NPost.parseToBoolean(request.GET.get('direction', True))
    round = int(request.GET.get('round', 1))

    from zr.index import find
    result = find(query, plan_id)
    result = [(item, len(Post.objects.filter(parent_id=item))) for item in result]
    paginator = Paginator(result, 25)

    try:
        actuall_item_list = paginator.page(round).object_list
    except EmptyPage:
        return []

    result = NPost.addDataToOutput(actuall_item_list)
    return result

@json_view
def date_search(request, plan_id, year, mon, day):
    from django.conf import settings
    import pytz
    from django.utils.timezone import make_aware,make_naive
    from django.db.models import Q

    round = int(request.GET.get('round',1))

    now = datetime.datetime(int(year),int(mon),int(day))
    delta = datetime.timedelta(days=1)

    start = make_aware(now,pytz.timezone(settings.TIME_ZONE))
    end = make_aware(now + delta,pytz.timezone(settings.TIME_ZONE))

    result = Post.objects.exclude(geometry=None)\
        .exclude(parent__isnull=False)\
        .filter(plan_id=int(plan_id))\
        .filter( Q(date__gte=start) & Q(date__lte=end))

    if len(result) == 0:
        return []
    result = [(item.id,len(Post.objects.filter(parent_id=item.id))) for item in result ]
    paginator = Paginator(result, 25);

    try:
        actuall_item_list = paginator.page(round).object_list
    except EmptyPage:
        return []

    return NPost.addDataToOutput(actuall_item_list)


class SubjectFeatPropertySerializer(ModelSerializer):
    class Meta:
        model = SubjectFeatProperty
        fields = ('key', 'value')


class SubjectFeatSerializer(GeoFeatureModelSerializer):
    feat_description = SubjectFeatPropertySerializer(many=True)
    description = serializers.CharField(default='')

    class Meta:
        model = SubjectFeat
        geo_field = "geom"
        fields = ('id', 'subject', 'color', 'geom', 'description', 'feat_description', )


class SubjectFeatList(generics.ListAPIView):
    queryset = SubjectFeat.objects.all()
    serializer_class = SubjectFeatSerializer

"""
class UserCountView(APIView):

    renderer_classes = (JSONRenderer)

    def get(self, request, format=None):
        user = User.objects.get(name=request.POST['user_name']);

        if not isinstance(user, get_user_model()):
            try:
                user = get_user(user)
                alt = six.text_type(user)
                url = avatar_url(user, size)
            except get_user_model().DoesNotExist:
                url = get_default_avatar_url()
                alt = _("Default Avatar")
        else:
            alt = six.text_type(user)
            url = avatar_url(user, size)
        context = dict(kwargs, **{
            'user': user,
            'url': url,
            'alt': alt,
            'size': size,
        })


        content = {'avatar_url': user_count}
        return Response(content)
"""

