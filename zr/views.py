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
from zr.models import Configuration


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

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return super(HomePageView,self).get(request, *args, **kwargs)

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
            user = User.objects.create_user(form.clean_username(),
                                            form.cleaned_data['email'],
                                            password=form.clean_password2())
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
        return render_to_response('zr/registration.html', {'form': form}, context_instance=RequestContext(request))


class DashboardView(View):


    def get(self, request):
        plan = request.GET.get('plan',1)
        context = RequestContext(request)
        context['configuration'] = Configuration.objects.get(plan=plan)
        return render_to_response('zr/dashboard/dashboard.html', {}, context_instance=context)




"""
class TestView(View):
    def get(self, request):
        from zr.api import SerializePost
        from zr.models import Post
        from rest_framework.renderers import JSONRenderer
        from django.http import HttpResponse
        import json
        all = {}
        roots = []
        for x in Post.objects.all():
            all[x.id] = {'obj': x, 'children': []}
        print all

        for k, d in all.items():
            obj = d['obj']
            if not obj.parent:
                roots.append(obj)
            else:
                all[obj.parent_id]['children'].append(obj)
        print roots

        post_json = json.dumps(roots)
        #post = Post.objects.get(id=2)
        #print post
        #post_s = SerializePost(post)
        #print post_s
        #post_json = post_s.data
        #print post_json
        return HttpResponse(JSONRenderer().render(roots), content_type='application/json')

"""
