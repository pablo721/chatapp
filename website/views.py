from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from chat.models import FriendList


class IndexView(TemplateView):
    template_name = 'website/index.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            return {'user': self.request.user}


class LoginView(TemplateView):
    template_name = 'website/login.html'
    form = AuthenticationForm

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            request.session.set_expiry(87600)
            login(request, user)
            return redirect('chat:chat')
        else:
            return render(request, 'website/login_failed.html')

    def get_context_data(self, **kwargs):
        return {'form': self.form}


class LogoutView(TemplateView):
    template_name = 'website/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name)


class SignupView(TemplateView):
    template_name = 'website/signup.html'
    form = UserCreationForm

    def post(self, request, *args, **kwargs):
        signup_form = self.form(request.POST)
        if signup_form.is_valid():
            form_data = signup_form.cleaned_data
            user = User.objects.create_user(username=form_data['username'], password=form_data['password1'])
            FriendList.objects.create(user=user)
            if user is not None:
                login(request, user)
                return redirect('website:index')
        else:
            print(f'Errors {signup_form.errors}')
            return render(request, 'website/signup_failed.html', {'errors': signup_form.errors})

    def get_context_data(self, **kwargs):
        return {'form': self.form}


class MonitorView(TemplateView):
    template_name = 'website/monitor.html'

