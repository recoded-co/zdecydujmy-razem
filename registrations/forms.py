# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class CustomLoginForm(AuthenticationForm):

    """Login form"""

    error_css_class = 'validation-error'
    required_css_class = 'validation-error'

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('np. jane lub jan@gmail.com'),
        })
    )

    password = forms.CharField(
        label=u'Hasło',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _(u'hasło'),
        }),
    )
