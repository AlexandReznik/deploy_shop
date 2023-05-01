from django.utils import timezone
from mainapp import models as mainapp_models
from .forms import ContactForm
from django.views.generic import TemplateView, ListView, View
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from mainapp import forms
from config.settings import RECIPIENTS_EMAIL
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Product, BasketItem, Category
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductModelSerializer, CategoryModelSerializer
from django.core.paginator import Paginator
from config import settings


def basket(request):
    basket_items = BasketItem.objects.all()
    total_price = sum(item.product.cost*item.quantity for item in basket_items)
    context = {'basket_items': basket_items, 'total_price': total_price}
    return render(request, 'mainapp/basket.html', context)


class MainPageView(ListView):
    template_name = "mainapp/index.html"
    paginate_by = 3
    context_object_name = 'objects'
    model = mainapp_models.Product
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context["objects"] = Product.objects.all()
        paginator = Paginator(context['objects'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


def product_list_by_category(request, category_id):
    products = Product.objects.filter(category=category_id)
    context = {'products': products}
    return render(request, 'mainapp/category_product.html', context)


class CategoryListView(ListView):
    template_name = 'mainapp/category.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context


class ProductDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Product, pk=pk)
        comments = post.comments.filter(approved_comment=True)
        form = forms.CommentForm()
        context = {'post': post, 'comments': comments, 'form': form}
        return render(request, 'mainapp/product_detail.html', context)

    def post(self, request, pk):
        post = get_object_or_404(Product, pk=pk)
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.created_date = timezone.now()
            comment.save()
            return redirect('mainapp:product_detail', pk=post.pk)
        comments = post.comments.filter(approved_comment=True)
        context = {'post': post, 'comments': comments, 'form': form}
        return render(request, 'mainapp/product_detail.html', context)


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
                messages.success(
                    request, _("Form submittet!"))
            except BadHeaderError:
                messages.warning(
                    request, _("Form not submitted!"))
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
    messages.success(
        request, _("Product has been added to your basket!"))
    if not created:
        basket_item.quantity += 1
        basket_item.save()

    return redirect('http://127.0.0.1:8000/mainapp/basket/')


def remove_from_basket(request, basket_item_id):
    basket_item = BasketItem.objects.get(id=basket_item_id)
    basket_item.delete()
    messages.success(
        request, _("Product has been removed from your basket!"))
    return redirect('http://127.0.0.1:8000/mainapp/basket/')


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class LogView(TemplateView):
    template_name = "mainapp/log_view.html"

    def get_context_data(self, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        with open(settings.LOG_FILE, "r") as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:  # first 1000 lines
                    break
                log_slice.insert(0, line)  # append at start
            context["log"] = "".join(log_slice)
        return context


class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))
