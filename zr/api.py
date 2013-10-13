from rest_framework import viewsets, routers
from rest_framework.serializers import ModelSerializer
from rest_framework import filters
from rest_framework import generics
from zr.models import Plan, Configuration, Geometry, Subjects, Post, Rate

class PlanViewSet(viewsets.ModelViewSet):
    model = Plan


class ConfigurationViewSet(viewsets.ModelViewSet):
    model = Configuration


class GeometryViewSet(viewsets.ModelViewSet):
    model = Geometry


class SubjectsViewSet(viewsets.ModelViewSet):
    model = Subjects

class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate

class PostSerializer(ModelSerializer):
    rate = RateSerializer(many=True)
    class Meta:
        model = Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

class RateListView(generics.ListAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = (filters.DjangoFilterBackend,)

class PostsListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_fields = ('id', 'author')


router = routers.DefaultRouter()
router.register(r'plans', PlanViewSet)
router.register(r'configurations', ConfigurationViewSet)
router.register(r'geometries', GeometryViewSet)
router.register(r'subjects', SubjectsViewSet)
router.register(r'posts', PostViewSet)
router.register(r'rates', RateViewSet)
#router.register(r'ratesfilter', RateListView)


