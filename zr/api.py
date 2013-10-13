from rest_framework import viewsets, routers
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from zr.models import Plan, Configuration, Geometry, Subjects, Post, Rate


class PlanViewSet(viewsets.ModelViewSet):
    model = Plan


class ConfigurationViewSet(viewsets.ModelViewSet):
    model = Configuration


class GeometryViewSet(viewsets.ModelViewSet):
    model = Geometry


class SubjectsViewSet(viewsets.ModelViewSet):
    model = Subjects


class SerializePost(Serializer):
    author = serializers.IntegerField()
    parent = serializers.IntegerField()
    plan = serializers.IntegerField()
    content = serializers.CharField(max_length=500)

    def __init__(self, *args, **kwargs):
        print 'lala'
        print args
        print kwargs
        super(SerializePost, self).__init__(self, *args, **kwargs)
        post = args[0]
        posts = post.comments.all()
        print '---'
        print type(posts)
        print '**'
        if posts:
            self.children = SerializePost(instance=posts, many=True)
"""
    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.author = attrs.get('author', instance.email)
            instance.parent = attrs.get('parent', instance.content)
            instance.plan = attrs.get('plan', instance.created)
            instance.content = attrs.get('content', instance.created)
            return instance
        return Post(**attrs)
"""

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


router = routers.DefaultRouter()
router.register(r'plans', PlanViewSet)
router.register(r'configurations', ConfigurationViewSet)
router.register(r'geometries', GeometryViewSet)
router.register(r'subjects', SubjectsViewSet)
router.register(r'posts', PostViewSet)
router.register(r'rates', RateViewSet)


