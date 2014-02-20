from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.gis.geos import WKTWriter
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.conf import settings
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None


class Profile(models.Model):
    user = models.ForeignKey(User)
    zipcode = models.CharField(max_length=6, null=True, blank=True)


class Geometry(models.Model):
    name = models.CharField(max_length=50)
    poly = models.PolygonField(null=True, blank=True)
    point = models.PointField(null=True, blank=True)
    objects = models.GeoManager()

    def geoElement(self):
        wkt = WKTWriter()
        if self.poly:
            return wkt.write(self.poly)
        elif self.point:
            return wkt.write(self.point)
        else:
            return None

    def geoId(self):
        posts = Post.objects.filter(geometry=self.id)
        if posts:
            return posts[0].id
        else:
            return None


class Plan(models.Model):
    name = models.CharField(max_length=50)
    center = models.PointField()
    zoom_level = models.IntegerField()
    after_search_zoom = models.IntegerField()
    geocoding_scope = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Subject(models.Model):
    label = models.CharField(max_length=50, null=True, blank=True)
    plan = models.ForeignKey(Plan, null=True, blank=True)

    def __unicode__(self):
        return self.label


class SubjectFeat(models.Model):
    subject = models.ForeignKey(Subject)
    geom = models.PolygonField(srid=4326)

    def getId(self):
        return self.id

    def getGeom(self):
        wkt = WKTWriter()
        if self.geom:
            return wkt.write(self.geom)
        else:
            return None


class SubjectFeatProperty(models.Model):
    feat = models.ForeignKey(SubjectFeat, related_name="properties")
    key = models.CharField(max_length=50)
    value = models.TextField()



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
        if self.max < self.min:
            raise ValidationError('max value can not be smolest then min value' )


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='comments')
    plan = models.ForeignKey(Plan, related_name='posts')
    content = models.TextField()
    geometry = models.ForeignKey(Geometry, null=True, blank=True)
    subscriptions = models.ManyToManyField(User, through="PostSubscription", null=True, blank=True)
    date = models.DateTimeField(auto_now=True, blank=True)

    def has_subscription(self, user=None):
        if user in self.subscriptions.all():
            return True
        else:
            return False

    def has_rate(self):
        rates = self.rates.all()
        count = len(rates)
        if count > 0:
            rate_sum = sum([x.rate if x.rate else 0 for x in rates])
            return rate_sum/count
        else:
            return 0

    def like_sum(self):
        rates = self.rates.filter(like=True)
        like_sum = sum([x.rate if x.like else -(x.rate) for x in rates])
        return like_sum

    def dislike_sum(self):
        rates = self.rates.filter(like=False)
        like_sum = sum([x.rate if x.like else x.rate for x in rates])
        return like_sum

    def has_likes(self):
        rates = self.rates.all()
        like_sum = sum([x.rate if x.like else -(x.rate) for x in rates])
        return like_sum

    def author_name(self):
        return self.author.username

    def get_root(self):
        if self.parent:
            return self.parent.get_root()
        else:
            return self


class Rate(models.Model):
    post = models.ForeignKey(Post, related_name='rates')
    user = models.ForeignKey(User)
    like = models.NullBooleanField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)

    def get_user_like(self, user):
        return Rate.objects.filter(user=user)

class PostSubscription(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    active = models.BooleanField()

    def get_user_subscriptions(self, user):
        return PostSubscription.objects.filter(user=user, active=True)

    def __unicode__(self):
        return '%s: %s' % (self.post.author, self.post.content)


class TrackEvents(models.Model):
    category = models.TextField()
    action = models.TextField(blank=True)
    opt_label = models.TextField(blank=True)
    opt_value = models.TextField(blank=True)
    opt_noninteraction = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return '%s: %s :  %s' % (self.category, self.action, self.date)


class WebNotification(models.Model):
    STATUS = (
        ('A',_('Alert')),
        ('AS', _('Alert seen')),
        ('I', _('Info')),
        ('IS', _('Info seen')),
    )
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS)

@receiver(post_save, sender=Post)
def post_notifications(sender, instance, created, **kwargs):
    root = instance.get_root()
    subscribed_users = root.subscriptions.all()
    if notification and len(subscribed_users) > 0:
        notification.send(subscribed_users, "post_new", {'plan': 'lolo', 'post_content': ''})

@receiver(post_save, sender=User)
def post_notifications(sender, instance, created, **kwargs):
    if created:
        p = Profile(user=instance, zipcode=None)
        p.save()


#@receiver(post_save, sender=User)
#def email_updater(sender, instance, created, **kwargs):
#    if created:
#        instance.email = instance.username
#        instance.save()
