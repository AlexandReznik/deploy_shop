from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('', views.MainPageView.as_view(), name='mainapp'),
    path('contacts/', views.contact_view, name='contacts'),
    path('<int:pk>/detail/', views.ProductDetail.as_view(), name='product_detail'),
    path('add_to_basket/<int:product_id>/',
         views.add_to_basket, name='add_to_basket'),
    path('remove_from_basket/<int:basket_item_id>/',
         views.remove_from_basket, name='remove_from_basket'),
    path('basket/', views.basket, name='basket'),
]
