from django.urls import path
from . import views

app_name='Store'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:user_id>', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('products/<str:search>', views.products, name='products'),
    path('category/<str:category>', views.category, name='category'),
    path('product/<str:pk>', views.detail, name='detail'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('legal-notice/', views.legal, name='legal'),
    path('tac/', views.tac, name='tac'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
]