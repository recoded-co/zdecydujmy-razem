from django.forms import ModelForm
from zr.models import PostSubscription
from django import forms
from django.utils.translation import ugettext_lazy as _


class PostSubscriptionForm(ModelForm):
    class Meta:
        model = PostSubscription


class ZipCodeForm(forms.Form):
    zipcode = forms.RegexField(max_length=6,
                               regex=r'^\d{2}-\d{3}$',
                               widget=forms.TextInput(),
                               label=_(u'zip code'),
                               required=True)
