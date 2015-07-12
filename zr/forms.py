# -*- coding: UTF-8 -*-
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from zr.models import PostSubscription, Profile


class PostSubscriptionForm(ModelForm):

    class Meta:
        model = PostSubscription
        exclude = ()


class ProfileForm(ModelForm):
    zipcode = forms.RegexField( max_length=6,
                               regex=r'^\d{2}-\d{3}$',
                               widget=forms.TextInput(),
                               label=_(u'Kod pocztowy *'),
                               required=True)
    source = forms.CharField(label=u'Skąd dowiedział się Pan(i) o konsultacjach? *',
                              widget=forms.RadioSelect(choices=Profile.SOURCES),
                              required=True)

    gender = forms.CharField(label=u"Płec", widget=forms.RadioSelect(choices=Profile.GENDER), required=False)

    education = forms.CharField(label=u'Wykształcenie',
                                 widget=forms.RadioSelect(choices=Profile.EDUCATION), required=False)

    job = forms.CharField(label=u'Aktualnie wykonywane zajęcie', widget=forms.RadioSelect(choices=Profile.JOB), required=False)

    gis_portals = forms.CharField(
        label=u'Czy korzysta Pan(i) z portali mapowych (np. Google Maps, OpenStreetMap, zumi.pl)?',
        widget=forms.RadioSelect(choices=Profile.YESNO), required=False)

    social_portals = forms.CharField(
        label=u'Czy korzysta Pan(i) z portali społecznościowych (np. Facebook, nk.pl)?',
        widget=forms.RadioSelect(choices=Profile.YESNO), required=False)

    class Meta:
        model = Profile
        fields = ('zipcode', 'source', 'gender', 'age', 'education', 'job', 'gis_portals', 'social_portals')
        exclude = ('first_login', 'user', )


class ZipCodeForm(forms.Form):

    zipcode = forms.RegexField(max_length=6,
                               regex=r'^\d{2}-\d{3}$',
                               widget=forms.TextInput(),
                               label=_(u'zip code'),
                               required=True)
