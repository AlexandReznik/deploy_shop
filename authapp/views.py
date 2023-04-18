from django.shortcuts import render
from django.contrib.auth.views import LoginView,  LogoutView
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from authapp import forms
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import UserUpdateForm


class RegisterView(CreateView):
    template_name = "authapp/register.html"
    model = get_user_model()
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy("mainapp:mainapp")


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _("See you later!"))
        return super().dispatch(request, *args, **kwargs)


# class ProfileView(TemplateView):
#     template_name = 'authapp/profile.html'


class ProfileView(View):
    form_class = UserUpdateForm
    template_name = 'authapp/profile.html'

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000/authapp/profile/')
        return render(request, self.template_name, {'form': form})
