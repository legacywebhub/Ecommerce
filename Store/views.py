from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items =  order.orderitem_set.all()
    else:
        items = []
        order = {
            'cart_total':0,
            'discount_total':0,
            'tax_total':0,
            'item_total':0,
            'total':0,
        }
    context = {
        'items':items,
        'order':order,
    }
    return render(request, 'cart.html', context)

def detail(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
    }
    return render(request, 'product_details.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        location = request.POST['location']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        try:
            email.index('@') and email.index('.')
        except ValueError:
            messages.info(request, 'Your email is not valid')
        else:
            message = Message.objects.create(name=name, location=location, email=email, subject=subject, message=message)
            message.save()
            messages.info(request, 'Your message was sent successfully')
            return redirect('Store:contact')    
    return render(request, 'contact.html')