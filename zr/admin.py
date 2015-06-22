from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin
from zr.models import *

admin.site.register(Geometry, admin.OSMGeoAdmin)
admin.site.register(Plan, admin.OSMGeoAdmin)
admin.site.register(Configuration)


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'date', 'is_removed')
    list_filter = ('is_removed',)
    search_fields = ('content',)

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
admin.site.register(SubjectFeat)
admin.site.register(SubjectFeatProperty)


class EventDecoration(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('category', 'action', 'opt_label', 'opt_value', 'opt_noninteraction', 'date')
    list_filter = ('category', 'action')
    search_fields = ['category', 'action', 'opt_label', 'opt_noninteraction']


admin.site.register(TrackEvents, EventDecoration)
