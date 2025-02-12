from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView, TemplateView
from django.contrib.auth import authenticate, login, logout, get_user_model

from authentication.forms import LoginUserForm, ProfileUserForm, RegisterUserForm


class AuthenticationUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('recipes:recipes_list')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('authentication:about_me')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        simple_group = Group.objects.get(name='Simple_user')
        user.groups.add(simple_group)
        login(request=self.request, user=user)
        return response


class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = "authentication/about_me.html"


class ProfileUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'authentication/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('authentication:about_me')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('authentication:login'))


def set_session_view(request: HttpRequest):
    request.session['foobar'] = 'spameggs'
    return HttpResponse('session set!')


def get_session_view(request: HttpRequest):
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'session value: {value!r}')
