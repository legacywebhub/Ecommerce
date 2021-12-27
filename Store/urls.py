from django.urls import path
from . import views

app_name='Store'
urlpatterns = [
    path('', views.index, name='index'),
    path('cart', views.cart, name='cart'),
    path('product/<str:pk>', views.detail, name='detail'),
    path('contact', views.contact, name='contact'),
]