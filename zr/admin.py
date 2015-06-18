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
admin.site.register(PostSubscription)
admin.site.register(Subject)
admin.site.register(SubjectFeat)
admin.site.register(SubjectFeatProperty)


class EventDecoration(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('category', 'action', 'opt_label', 'opt_value', 'opt_noninteraction', 'date')
    list_filter = ('category', 'action')
    search_fields = ['category', 'action', 'opt_label', 'opt_noninteraction']


admin.site.register(TrackEvents, EventDecoration)
