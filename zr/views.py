from django.views.generic.base import TemplateView, View
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class LoginForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(), required=True)
    first_name = forms.CharField(max_length=30,
                               widget=forms.TextInput(),
                               label=_(u'first name'), required=False)
    last_name = forms.CharField(max_length=30,
                               widget=forms.TextInput(),
                               label=_(u'last name'), required=False)

class HomePageView(TemplateView):
    template_name = "zr/index.html"

    def get_context_data(self, **kwargs):
        from django.contrib.auth.forms import AuthenticationForm
        from zdecydujmyrazem import settings
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['form'] = AuthenticationForm()
        context['next'] = settings.LOGIN_REDIRECT_URL
        return context


class UserCreationPageView(TemplateView):
    template_name = "zr/registration.html"

    def get_context_data(self, **kwargs):
        from zdecydujmyrazem import settings
        context = super(UserCreationPageView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        context['next'] = settings.LOGIN_REDIRECT_URL
        return context

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.clean_username(), form.cleaned_data['email'], password=form.clean_password2())
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
        return render_to_response('zr/registration.html', { 'form': form }, context_instance=RequestContext(request))


class DashboardView(View):

    def get(self, request):
        return render_to_response('zr/dashboard/dashboard.html', {}, context_instance=RequestContext(request))


