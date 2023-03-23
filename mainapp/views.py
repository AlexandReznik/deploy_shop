from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from mainapp import models as mainapp_models
from .forms import ContactForm
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from mainapp import forms as mainapp_forms
from config.settings import RECIPIENTS_EMAIL
from django.urls import reverse_lazy
# Create your views here.


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context["objects"] = mainapp_models.Goods.objects.all()
        return context


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email_address = form.cleaned_data['email_address']
            message = form.cleaned_data['message']
            try:
                send_mail(f'Message from {email_address} - {first_name}', message,
                          email_address, RECIPIENTS_EMAIL)
                messages.add_message(
                    request, messages.INFO, _("Form submittet!"))
            except BadHeaderError:
                messages.add_message(
                    request, messages.WARNING, _("Form not submitted!"))
                return HttpResponse('Error.')
            return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))
    else:
        return HttpResponse('Incorrect request')
    return render(request, "mainapp/contact.html", {'form': form})
# class GoodsListView(ListView):
#     template_name = "mainapp/index.html"

    # def get_context_data(self, **kwargs):
    #     context = super(GoodsListView, self).get_context_data(**kwargs)
    #     context["objects"] = mainapp_models.Goods.objects.all()
    #     return context
