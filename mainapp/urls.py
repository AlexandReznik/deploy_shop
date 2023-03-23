from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('', views.MainPageView.as_view(), name="mainapp"),
    path('contacts/', views.contact_view, name='contacts'),
]
