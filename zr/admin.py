from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin
from zr.models import *
from django.http import HttpResponse
from rest_framework import serializers
import json

admin.site.register(Geometry, admin.OSMGeoAdmin)
admin.site.register(Plan, admin.OSMGeoAdmin)
admin.site.register(Configuration)

class GeometrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Geometry
        fields = ('id', 'name', 'poly', 'point', 'line')

class UserSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return instance.username


class PostSerializer(serializers.ModelSerializer):

    author = UserSerializer()
    subscriptions = serializers.StringRelatedField(many=True)
    geometry = GeometrySerializer()

    def to_representation(self, obj):
        self.fields['comments'] = PostSerializer(obj, many=True)
        return super(PostSerializer, self).to_representation(obj)

    class Meta:
        model = Post
        fields = ('author', 'plan', 'content', 'geometry', 'date', 'is_removed', 'subscriptions')

def export_to_json(modeladmin, request, queryset):

    data = PostSerializer(queryset, many=True)

    result = data.data

    response = HttpResponse(json.dumps(result), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="objects.json"'

    return response

export_to_json.short_description = "Export selected posts to JSON file"

class PostAdmin(admin.ModelAdmin):

    list_display = ('author', 'date', 'is_removed')
    list_filter = ('is_removed',)
    search_fields = ('content',)
    actions = [export_to_json]

admin.site.register(Post, PostAdmin)

admin.site.register(Rate)


class PostSubscriptionAdmin(admin.ModelAdmin):
    model = PostSubscription
    list_display = ('user', 'get_post', 'get_author', 'active',)

    def get_queryset(self, request):
        return super(PostSubscriptionAdmin, self).get_queryset(request).select_related('user', 'post', 'post__author')

    def get_post(self, obj):
        return obj.post.content

    get_post.short_description = 'Post'
    get_post.admin_order_field = 'post'

    def get_author(self, obj):
        return obj.post.author

    get_author.short_description = 'Author'
    get_author.admin_order_field = 'post__author'


admin.site.register(PostSubscription, PostSubscriptionAdmin)

admin.site.register(Subject)


class SubjectFeatAdmin(admin.ModelAdmin):
    model = SubjectFeat
    list_display = ('subject', 'get_geom', 'color')

    def get_geom(self, obj):
        return str(obj.geom)[:200]

    get_geom.short_description = 'Geometry'
    get_geom.admin_order_field = 'geom'


admin.site.register(SubjectFeat, SubjectFeatAdmin)

admin.site.register(SubjectFeatProperty)


class EventDecoration(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('category', 'action', 'opt_label', 'opt_value', 'opt_noninteraction', 'date')
    list_filter = ('category', 'action')
    search_fields = ['category', 'action', 'opt_label', 'opt_noninteraction']


admin.site.register(TrackEvents, EventDecoration)


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('action', 'user', 'obj', 'created_at')
    list_filter = ('action', 'user')
    search_fields = ['action', 'user', 'obj']


admin.site.register(Event, EventAdmin)




