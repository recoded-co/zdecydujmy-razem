from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Geometry(models.Model):
    name = models.CharField(max_length=50)
    poly = models.PolygonField()
    objects = models.GeoManager()


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


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='comments')
    plan = models.ForeignKey(Plan, related_name='posts')
    content = models.TextField()


class Rate(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    like = models.NullBooleanField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)


@receiver(post_save, sender=User)
def email_updater(sender, instance, created, **kwargs):
    if created:
        instance.email = instance.username
        instance.save()
