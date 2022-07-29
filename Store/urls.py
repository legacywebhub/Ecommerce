from django.urls import path, reverse_lazy
from . import views
# For password reset
from django.contrib.auth import views as auth_views

app_name='Store'
urlpatterns = [
    # Page urls and paths
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('products/<str:search>', views.products, name='products'),
    path('category/<str:category>', views.category, name='category'),
    path('special-offer/', views.specialOffer, name='special'),
    path('product/<str:pk>', views.detail, name='detail'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('legal-notice/', views.legal, name='legal'),
    path('tac/', views.tac, name='tac'),
    path('checkout/', views.checkout, name='checkout'),

    # Pseudo urls and paths
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),

    # Authentication url and paths
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:user_id>', views.profile, name='profile'),

    # Password reset paths
    path('reset-password/', 
    auth_views.PasswordResetView.as_view(
    template_name="password_reset.html",
    success_url=reverse_lazy('password_reset_done')
    ), 
    name="reset_password"),

    path('reset-password-sent/', 
    auth_views.PasswordResetDoneView.as_view(
    template_name="password_reset_sent.html"
    ), 
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(
    template_name="password_reset_form.html",
    success_url=reverse_lazy('password_reset_complete')
    ), 
    name="password_reset_confirm"),

    path('password-reset-complete', 
    auth_views.PasswordResetCompleteView.as_view(
    template_name="password_reset_complete.html"
    ), 
    name="password_reset_complete"),
]