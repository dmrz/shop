from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView


class FrontendLoginView(LoginView):
    template_name = 'core/frontend_login.html'


class FrontendView(LoginRequiredMixin, TemplateView):
    template_name = 'core/frontend.html'
