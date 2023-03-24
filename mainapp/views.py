from django.shortcuts import render
from mainapp import models as mainapp_models
from .forms import ContactForm
from django.views.generic import TemplateView, DetailView
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from mainapp import forms
from config.settings import RECIPIENTS_EMAIL
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib import messages
from django.forms import modelform_factory
from .models import Product, BasketItem
from .forms import BasketForm


def basket(request):
    basket_items = BasketItem.objects.all()
    context = {'basket_items': basket_items}
    return render(request, 'mainapp/basket.html', context)


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context["objects"] = Product.objects.all()
        return context


class ProductDetail(DetailView):
    template_name = 'mainapp/product_detail.html'
    model = Product


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


def add_to_basket(request, product_id):
    product = Product.objects.get(id=product_id)
    basket_item, created = BasketItem.objects.get_or_create(
        # user=request.user,
        product=product
    )
    if not created:
        basket_item.quantity += 1
        basket_item.save()
        messages.success(
            request, 'Product has been added to your basket!')
    return redirect('/')


def remove_from_basket(request, basket_item_id):
    basket_item = BasketItem.objects.get(id=basket_item_id)
    basket_item.delete()
    messages.success(request, 'Product has been removed from your basket!')
    return redirect('/')
