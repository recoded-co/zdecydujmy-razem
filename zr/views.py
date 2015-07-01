# -*- coding: UTF-8 -*-
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DeleteView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

from registrations.forms import CustomLoginForm
from zr.models import Profile
from zr.models import Configuration, PostSubscription, Plan
from zr.forms import ZipCodeForm, ProfileForm
from avatar.models import Avatar
from avatar.forms import PrimaryAvatarForm, DeleteAvatarForm, UploadAvatarForm
from avatar.views import _get_avatars, _get_next
from django.contrib import messages
from avatar.signals import avatar_updated
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class LoginForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(), required=True)
    first_name = forms.CharField(max_length=30,
                               widget=forms.TextInput(),
                               label=_(u'first name'), required=False)
    last_name = forms.CharField(max_length=30,
                               widget=forms.TextInput(),
                               label=_(u'last name'), required=False)
    #zipcode = forms.RegexField(max_length=30,
    #                          regex=r'^\d{2}-\d{3}$',
    #                           widget=forms.TextInput(),
    #                           label=_(u'zip code'), required=True)


class HomePageView(TemplateView):
    template_name = "zr/index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return super(HomePageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        from zdecydujmyrazem import settings
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['form'] = CustomLoginForm()
        context['next'] = settings.LOGIN_REDIRECT_URL
        return context


class UserCreationPageView(TemplateView):
    template_name = "zr/registration.html"

    def get_context_data(self, **kwargs):
        from zdecydujmyrazem import settings
        context = super(UserCreationPageView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        context['next'] = settings.LOGIN_REDIRECT_URL# TODO czy jest next w parametrach
        return context

    def post(self, request):
        from django.contrib.auth import authenticate, login
        form = LoginForm(request.POST)

        if form.is_valid():
            try:
                user = User.objects.get(email__iexact = form.cleaned_data['email'])
                raise User.MultipleObjectsReturned
            except User.DoesNotExist:
                pass
            except User.MultipleObjectsReturned:
                from django.forms.util import ErrorList
                errors = form._errors.setdefault("email", ErrorList())
                errors.append(u"Email alredy exist")
                return render_to_response('zr/registration.html', {'form': form}, context_instance=RequestContext(request))

            user = User.objects.create_user(form.clean_username(),
                                            form.cleaned_data['email'],
                                            password=form.clean_password2())
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()


            #profile = user.profile
            #profile.zipcode = form.cleaned_data['zipcode']
            #profile.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            return HttpResponseRedirect(reverse('zipcode_check'))
        return render_to_response('zr/registration.html', {'form': form}, context_instance=RequestContext(request))


class DashboardView(View):

    def get(self, request):
        plan_id = request.GET.get('plan', 1)
        configuration = Configuration.objects.get(plan=plan_id)
        plan = Plan.objects.get(id=plan_id)
        return render_to_response('zr/dashboard/dashboard.html',
                                  {'configuration': configuration, 'plan_id': plan_id, 'plan': plan},
                                  context_instance=RequestContext(request))


class ZipcodeCheckView(View):

    def get(self, request):
        from django.conf import settings
        user = request.user

        try:
            profile = user.profile
        except Profile.DoesNotExist, e:
            profile = Profile(user=user)
            profile.save()

        next = request.GET.get('next', settings.HOME_PAGE_URL)# TODO hardcoded next
        if profile and not profile.first_login:
            return redirect(next)
        else:
            form = ProfileForm(initial={'user': request.user, 'zipcode': profile.zipcode if profile.zipcode else ''})
            return render_to_response('zr/zip_code.html', {'form': form, 'next': next}, context_instance=RequestContext(request))

    def post(self, request):
        profile = request.user.profile
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile.zipcode = form.cleaned_data['zipcode']
            profile.user = request.user
            profile.first_login = False
            profile.save()
            return redirect(request.POST['next'])
        return render_to_response('zr/zip_code.html', {'form': form, 'next': request.POST['next']}, context_instance=RequestContext(request))

@login_required
def change2(request, extra_context=None, next_override=None,
           upload_form=UploadAvatarForm, primary_form=PrimaryAvatarForm,
           *args, **kwargs):
    if extra_context is None:
        extra_context = {}
    avatar, avatars = _get_avatars(request.user)
    if avatar:
        kwargs = {'initial': {'choice': avatar.id}}
    else:
        kwargs = {}
    upload_avatar_form = upload_form(user=request.user, **kwargs)
    primary_avatar_form = primary_form(request.POST or None,
                                       user=request.user,
                                       avatars=avatars, **kwargs)
    if request.method == "POST":
        updated = False
        if 'choice' in request.POST and primary_avatar_form.is_valid():
            avatar = Avatar.objects.get(
                id=primary_avatar_form.cleaned_data['choice'])
            avatar.primary = True
            avatar.save()
            updated = True
            messages.success(request, _("Successfully updated your avatar."))
        if updated:
            avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)
        return redirect(next_override or _get_next(request))

    context = {
        'avatar': avatar,
        'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
        'primary_avatar_form': primary_avatar_form,
        'next': next_override or _get_next(request)
    }
    context.update(extra_context)
    return render(request, 'zr/avatar/change.html', context)
