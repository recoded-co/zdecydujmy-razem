from django.views.generic.base import TemplateView, View
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm

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
        context['form'] = UserCreationForm()
        context['next'] = settings.LOGIN_REDIRECT_URL
        return context

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render_to_response('zr/index.html', {}, context_instance=RequestContext(request))
        return render_to_response('zr/registration.html', {'form': form },context_instance=RequestContext(request))


class DashboardView(View):

    def get(self, request):
        return render_to_response('zr/dashboard/dashboard.html', {}, context_instance=RequestContext(request))


