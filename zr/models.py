from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.gis.geos import WKTWriter
from django.core.exceptions import ValidationError


class Geometry(models.Model):
    name = models.CharField(max_length=50)
    poly = models.PolygonField(null=True, blank=True)
    point= models.PointField(null=True, blank=True)
    objects = models.GeoManager()

    def geoElement(self):
        wkt = WKTWriter()
        if(self.poly):
            return wkt.write(self.poly)
        elif(self.point):
            return wkt.write(self.point)
        else:
            return None


class Plan(models.Model):
    name = models.CharField(max_length=50)
    area = models.PolygonField()
    geometries = models.ManyToManyField(Geometry, through='Subjects')
    zoom_level = models.IntegerField()


class Subjects(models.Model):
    geometry = models.ForeignKey(Geometry)
    plan = models.ForeignKey(Plan)
    label = models.CharField(max_length=50, null=True, blank=True)


class Configuration(models.Model):
    side = (
        ('L', _('Left side bar')),
        ('R', _('Right side bar')),
    )
    plan = models.ForeignKey(Plan, related_name='configuration')
    side = models.CharField(max_length=1, choices=side)
    max = models.IntegerField()
    min = models.IntegerField()
    default = models.IntegerField()

    def clean(self):
        if self.max > 100 or self.max < 0:
            raise ValidationError('max value bad range (0,100)')
        if self.min > 100 or self.min < 0:
            raise ValidationError('min value bad range (0,100)')
        if self.max< self.min:
            raise ValidationError('max value can not be smolest then min value' )

class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='comments')
    plan = models.ForeignKey(Plan, related_name='posts')
    content = models.TextField()
    geometry = models.ForeignKey(Geometry, null=True, blank=True)

    def has_rate(self):
        rates = self.rates.all()
        count = len(rates)
        if count > 0:
            rate_sum = sum([x.rate if x.rate else 0 for x in rates])
            return rate_sum/count
        else:
            return 0

    def has_likes(self):
        rates = self.rates.all()
        like_sum = sum([x.rate if x.like else -(x.rate) for x in rates])
        return like_sum

    def author_name(self):
        return self.author.username;



class Rate(models.Model):
    post = models.ForeignKey(Post, related_name='rates')
    user = models.ForeignKey(User)
    like = models.NullBooleanField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)


#@receiver(post_save, sender=User)
#def email_updater(sender, instance, created, **kwargs):
#    if created:
#        instance.email = instance.username
#        instance.save()
