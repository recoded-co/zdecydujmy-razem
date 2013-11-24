__author__ = 'marcinra'
from django.forms import forms
from django.utils.translation import ugettext as _


class DocumentForm(forms.Form):
    datafile = forms.FileField(
        label=_('Wybierz plik'),
        help_text=_('max. 42 megabajtow')
    )