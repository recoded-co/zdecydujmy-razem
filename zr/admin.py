from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin
from zr.models import *

admin.site.register(Geometry, admin.OSMGeoAdmin)
admin.site.register(Plan, admin.OSMGeoAdmin)
admin.site.register(Configuration)
admin.site.register(Post)
admin.site.register(Rate)
admin.site.register(PostSubscription)
admin.site.register(Subject)
admin.site.register(SubjectFeat)
admin.site.register(SubjectFeatProperty)


class EventDecoration(admin.ModelAdmin):
    list_display = ('category', 'action','opt_label','opt_value','opt_noninteraction','date')

admin.site.register(TrackEvents, EventDecoration)
