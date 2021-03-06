from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin
from zr.models import *

admin.site.register(Geometry, admin.OSMGeoAdmin)
admin.site.register(Plan, admin.OSMGeoAdmin)
admin.site.register(Subjects)
admin.site.register(Configuration)
admin.site.register(Post)
admin.site.register(Rate)
admin.site.register(PostSubscription)
