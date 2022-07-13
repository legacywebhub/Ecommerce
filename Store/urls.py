from django.urls import path
from . import views

app_name='Store'
urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('products/<str:search>', views.products, name='products'),
    path('category/<str:category>', views.category, name='category'),
    path('product/<str:pk>', views.detail, name='detail'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
]