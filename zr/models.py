# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.gis.geos import WKTWriter
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import connection
from django import forms
from datetime import datetime
from zr import index


from django.conf import settings
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None


class Profile(models.Model):
    SOURCES = (
        ('media', u'Z mediów'),
        ('ulotka_poczta', u'Z ulotki przesłanej pocztą'),
        ('facebook', u'Z facebooka'),
        ('ulotka_bezp', u'Z bezpośrednio otrzymanej ulotki'),
        ('znajomi', u'Od znajomych'),
        ('inne', u'Z innego źródła')
    )
    GENDER = (
        ('k', u'Kobieta'),
        ('m', u'Mężczyzna')
    )
    EDUCATION = (
        ('podstawowe', u'Podstawowe'),
        ('gimnazjalne', u'Gimnazjalne'),
        ('zawodowe', u'Zasadnicze zawodowe'),
        ('srednie', u'Średnie'),
        ('wyzsze', u'Wyższe')
    )
    JOB = (
        ('uczen', u'Uczeń'),
        ('student', u'Student'),
        ('administracja', u'Pracownik administracji publicznej'),
        ('etat', u'Zatrudniony w prywatnej firmie'),
        ('przedsiebiorca', u'Przedsiębiorca/ właściciel firmy'),
        ('wolny', u'Wolny zawód'),
        ('emeryt', u'Emeryt/ rencista'),
        ('bezrobotny', u'Nie pracujący'),
        ('inne', u'Inne zajęcie')
    )
    YESNO = (
        ('tak', _('Tak')),
        ('nie', _('Nie'))
    )

    first_login = models.BooleanField(default=True)

    user = models.OneToOneField(User)

    zipcode = models.CharField(u'Kod pocztowy',
                               max_length=6, null=True, blank=True)

    source = models.CharField(u'Skąd dowiedział się Pan(i) o konsultacjach?',
                              max_length=13, choices=SOURCES, null=True, blank=True)

    gender = models.CharField(u'Płeć',
                              max_length=1, choices=GENDER, null=True, blank=True)

    age = models.IntegerField(u'Wiek', blank=True, null=True)

    education = models.CharField(u'Wykształcenie',
                                 max_length=11, choices=EDUCATION, null=True, blank=True)

    job = models.CharField(u'Aktualnie wykonywane zajęcie',
                           max_length=13, choices=JOB, null=True, blank=True)

    gis_portals = models.CharField(
        u'Czy korzysta Pan(i) z portali mapowych (np. Google Maps, OpenStreetMap, zumi.pl)?',
        max_length=13, choices=YESNO, null=True, blank=True)

    social_portals = models.CharField(
        u'Czy korzysta Pan(i) z portali społecznościowych (np. Facebook, nk.pl)?',
        max_length=13, choices=YESNO, null=True, blank=True)


class Geometry(models.Model):
    name = models.CharField(max_length=50)
    poly = models.PolygonField(null=True, blank=True)
    point = models.PointField(null=True, blank=True)
    line = models.LineStringField(null=True, blank=True)
    objects = models.GeoManager()

    def geoElement(self):
        wkt = WKTWriter()
        if self.poly:
            return wkt.write(self.poly)
        elif self.point:
            return wkt.write(self.point)
        elif self.line:
            return wkt.write(self.line)
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
    color = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    """
    def getId(self):
        return self.id

    def getGeom(self):
        wkt = WKTWriter()
        if self.geom:
            return wkt.write(self.geom)
        else:
            return None
    """


class SubjectFeatProperty(models.Model):
    feat = models.ForeignKey(SubjectFeat, related_name="feat_description")
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
    date = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False)

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

"""    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.date = datetime.now()

        return super(Post, self).save(*args, **kwargs)

    def numcom(self):
        return self.pk #cursor.fetchone()

    def save(self, *args, **kwargs):
        print 'save is calling'
        return super(Post, self).save(*args, **kwargs)
    """


class Rate(models.Model):
    post = models.ForeignKey(Post, related_name='rates')
    user = models.ForeignKey(User)
    like = models.NullBooleanField(null=True, blank=True, default=False)
    rate = models.IntegerField(null=True, blank=True)

    def get_user_like(self, user):
        return Rate.objects.filter(user=user)


class PostSubscription(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    active = models.BooleanField(default=False)

    def get_user_subscriptions(self, user):
        return PostSubscription.objects.filter(user=user, active=True)

    def __unicode__(self):
        return '%s: %s' % (self.post.author, self.post.content)

class Event(models.Model):
    ACTION_UKO = 'UKO'
    ACTION_UAO = 'UAO'
    ACTION_UDO = 'UDO'
    ACTION_UST = 'UST'
    ACTION_UWD = 'UWD'
    ACTION_USD = 'USD'
    ACTION_USK = 'USK'
    ACTION_UFSA = 'UFSA'
    ACTION_UFSD = 'UFSD'
    ACTION_ULO = 'ULO'
    ACTION_UDP = 'UDP'
    ACTION_UPP = 'UPP'
    ACTION_MI = 'MI'
    ACTION_ZSZ = 'ZSZ'
    ACTION_ZSL = 'ZSL'
    ACTION_ZCA = 'ZCA'
    ACTION_MPZPZ = 'MPZPZ'
    ACTION_MPZPO = 'MPZPO'
    ACTION_STUDZ = 'STUDZ'
    ACTION_STUDO = 'STUDO'
    ACTION_MPZS = 'MPZS'
    ACTION_MPMA = 'MPMA'
    ACTION_UDP = 'UDP'
    ACTION_UDPA = 'UDPA'
    ACTION_UDO = 'UDO'
    ACTION_UDOA = 'UDOA'
    ACTION_UDL = 'UDL'
    ACTION_UDLA = 'UDLA'
    ACTION_UFPP = 'UFPP'
    ACTION_UFPO = 'UFPO'
    ACTION_WWPO = 'WWPO'
    ACTION_WOZM = 'WOZM'
    ACTION_ZZOM = 'ZZOM'
    ACTION_ZZSR = 'ZZSR'
    ACTION_WAPM = 'WAPM'
    ACTION_IOMP = 'IOMP'
    ACTION_POM = 'POM'
    ACTION_WFPP = 'WFPP'
    ACTION_DWDC = 'DWDC'

    ACTION_CHOICES = (
        (ACTION_UKO, _('UKO')),
        (ACTION_UAO, _('UAO')),
        (ACTION_UDO, _('UDO')),
        (ACTION_UST, _('UST')),
        (ACTION_UWD, _('UWD')),
        (ACTION_USD, _('USD')),
        (ACTION_USK, _('USK')),
        (ACTION_UFSA, _('UFSA')),
        (ACTION_UFSD, _('UFSD')),
        (ACTION_ULO, _('ULO')),
        (ACTION_UDP, _('UDP')),
        (ACTION_UPP, _('UPP')),
        (ACTION_MI, _('MI')),
        (ACTION_ZSZ, _('ZSZ')),
        (ACTION_ZSL, _('ZSL')),
        (ACTION_ZCA, _('ZCA')),
        (ACTION_MPZPZ, _('MPZPZ')),
        (ACTION_MPZPO, _('MPZPO')),
        (ACTION_STUDZ, _('STUDZ')),
        (ACTION_STUDO, _('STUDO')),
        (ACTION_MPZS, _('MPZS')),
        (ACTION_MPMA, _('MPMA')),
        (ACTION_UDP, _('UDP')),
        (ACTION_UDPA, _('UDPA')),
        (ACTION_UDO, _('UDO')),
        (ACTION_UDOA, _('UDOA')),
        (ACTION_UDL, _('UDL')),
        (ACTION_UDLA, _('UDLA')),
        (ACTION_UFPP, _('UFPP')),
        (ACTION_UFPO, _('UFPO')),
        (ACTION_WWPO, _('WWPO')),
        (ACTION_WOZM, _('WOZM')),
        (ACTION_ZZOM, _('ZZOM')),
        (ACTION_ZZSR, _('ZZSR')),
        (ACTION_WAPM, _('WAPM')),
        (ACTION_IOMP, _('IOMP')),
        (ACTION_POM, _('POM')),
        (ACTION_WFPP, _('WFPP')),
        (ACTION_DWDC, _('DWDC')),
    )

    action = models.CharField(max_length=16, choices=ACTION_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    obj = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


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
def post_notifications(sender, instance, **kwargs):
    root = instance.get_root()
    subscribed_users = root.subscriptions.all()
    if notification and len(subscribed_users) > 0:
        print 'notify: %s' % str(subscribed_users)
        notification.send(subscribed_users, "post_new", {'plan': instance.plan, 'post_content': instance.content})
    index.update_index(instance)


@receiver(post_save, sender=User)
def ZipCodeUpdate(sender, instance, created, **kwargs):
    if created:
        p = Profile(user=instance, zipcode=None)
        p.save()


#@receiver(post_save, sender=User)
#def email_updater(sender, instance, created, **kwargs):
#    if created:
#        instance.email = instance.username
#        instance.save()
