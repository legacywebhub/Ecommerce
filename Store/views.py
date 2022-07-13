from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from datetime import datetime
from django.conf import settings

# General variables
categories = Category.objects.all()
hot_products = Product.objects.filter(hot=True).order_by('?')[:3]

# Create your views here.
def index(request):
    p = Paginator(Product.objects.all(), 3)
    page = request.GET.get('page')
    products = p.get_page(page)
    
    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        # Creating a customer using his device ID from browser
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items =  order.orderitem_set.all()
    item_total = order.item_total
    total = order.total


    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'products': products,
        'item_total': item_total,
        'total': total,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'index.html', context)


def products(request, search):
    products_list = Product.objects.filter(name__contains=search)
    products_count = products_list.count
    p = Paginator(products_list, 3)
    page = request.GET.get('page')
    products = p.get_page(page)
    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        # Creating a customer using his device ID from browser
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    item_total = order.item_total
    total = order.total
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {
        'search':search,
        'products':products,
        'products_count':products_count,
        'item_total': item_total,
        'total': total,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'products.html', context)



def category(request, category):
    products_list = Product.objects.filter(category=category)
    category = ProductCategory.objects.get(id=category)
    products_count = products_list.count
    p = Paginator(products_list, 3)
    page = request.GET.get('page')
    products = p.get_page(page)
    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        # Creating a customer using his device ID from browser
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    item_total = order.item_total
    total = order.total
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {
        'products':products,
        'products_count':products_count,
        'item_total': item_total,
        'total': total,
        'category': category,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'product-category.html', context)


def cart(request):
    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        # Creating a customer using his device ID from browser
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items =  order.orderitem_set.all()
    item_total = order.item_total
    total = order.total
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'items':items,
        'order':order,
        'item_total': item_total,
        'total': total,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'cart.html', context)

def detail(request, pk):
    product = Product.objects.get(id=pk)
    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        # Creating a customer using his device ID from browser
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    item_total = order.item_total
    total = order.total
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    context = {
        'product': product,
        'item_total': item_total,
        'total':total,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'product_details.html', context)

def contact(request):
    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        # Creating a customer using his device ID from browser
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    item_total = order.item_total
    total = order.total

    if request.method == 'POST':
        if 'search' in request.POST:
            search = request.POST['search']
            return redirect('/products/'+search)
        elif 'message' in request.POST:
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

    context = {'item_total':item_total, 'total':total}
    return render(request, 'contact.html', context)

def checkout(request):
    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        # Creating a customer using his device ID from browser
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items =  order.orderitem_set.all()
    item_total = order.item_total
    total = order.total

    context = {
        'items':items,
        'order':order, 
        'item_total': item_total, 
        'total':total, 
        'customer':customer, 
        'public_key': settings.PUBLIC_KEY,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('product',productId)
    print('action',action)
    
    # Getting product
    product = Product.objects.get(id=productId)

    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        # Creating a customer using his device ID from browser
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)


    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    

    # Determines what action to take
    if action == 'subtract':
        orderItem.quantity -= 1
    elif action == 'add':
        orderItem.quantity += 1
    elif action == 'delete':
        orderItem.delete()
        
    orderItem.save()
    
    # Deleting item if quantity is less than 1
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was manipulated', safe=False)


def processOrder(request):
    # Generation a unique code used as transaction id
    # transaction_id = datetime.now().timestamp().replace('.', '')
    data = json.loads(request.body)
    print('data:', data)
    first_name = data['shippingFormData']['first-name']
    last_name = data['shippingFormData']['last-name']
    phone2 = data['shippingFormData']['phone2']

    # Checking to see if phone2 is empty since it isn't mandactory
    # Set as None if an empty string
    if phone2 == '':
        phone2 = None

    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        # Creating a customer using his device ID from browser
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
        # Populating the customer field
        customer.name = f'{first_name} {last_name}'
        customer.email = data['shippingFormData']['email']
        customer.save()
        print('customer saved')
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order.transaction_id = data['shippingFormData']['transaction-id']
    total = data['shippingFormData']['total']

    # Making sure total on the frontend equals total on the backend
    # Frontend may be manipulated using browser inspection tool
    if total == order.total:
        order.complete = True
    order.save()

    print('order saved')

    # Saving shipping detail of customer
    if order.shipping == True:
        shipping_details = ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shippingFormData']['address'],
            apartment=data['shippingFormData']['apartment'],
            city=data['shippingFormData']['city'],
            state=data['shippingFormData']['state'],
            country=data['shippingFormData']['country'],
            zipcode=data['shippingFormData']['zipcode'],
            phone1=data['shippingFormData']['phone1'],
            phone2=phone2,
        )
        shipping_details.save()

    print('shipping details saved')
    
    return JsonResponse('Payment submitted...', safe=False)