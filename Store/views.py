from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import JsonResponse
import json
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    if request.method == 'POST':
        search = request.POST['search']
        print(search)
        return redirect('/products/'+search)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items =  order.orderitem_set.all()
        item_total = order.item_total
        total = order.total
    else:
        '''
        This is for non logged in users. 
        Temporal solution for error generated when user isn't logged in
        '''
        items = []
        order = {
            'cart_total':0,
            'discount_total':0,
            'tax_total':0,
            'item_total':0,
            'total':0,
        }
        item_total = order['item_total']
        total = order['total']
    #   products = Product.objects.all().order_by('?')
    p = Paginator(Product.objects.all(), 3)
    page = request.GET.get('page')
    products = p.get_page(page)
    context = {
        'products': products,
        'item_total': item_total,
        'total': total,
    }
    return render(request, 'index.html', context)


def products(request, search):
    products_list = Product.objects.filter(name__contains=search) or Product.objects.filter(category=search)
    products_count = products_list.count
    p = Paginator(products_list, 3)
    page = request.GET.get('page')
    products = p.get_page(page)
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {'search':search,'products':products,'products_count':products_count}
    return render(request, 'products.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items =  order.orderitem_set.all()
        item_total = order.item_total
        total = order.total
    else:
        '''
        This is for non logged in users. 
        Temporal solution for error generated when user isn't logged in
        '''
        items = []
        order = {
            'cart_total':0,
            'discount_total':0,
            'tax_total':0,
            'item_total':0,
            'total':0,
        }
        item_total = order['item_total']
        total = order['total']
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    context = {
        'items':items,
        'order':order,
        'item_total': item_total,
        'total': total
    }
    return render(request, 'cart.html', context)

def detail(request, pk):
    product = Product.objects.get(id=pk)
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    context = {
        'product': product,
    }
    return render(request, 'product_details.html', context)

def contact(request):
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

    return render(request, 'contact.html')

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items =  order.orderitem_set.all()
    else:
        '''
        This is for non logged in users. 
        Temporal solution for error generated when user isn't logged in
        '''
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
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('product',productId)
    print('action',action)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    

    if action == 'remove':
        orderItem.quantity = orderItem.quantity - 1
        return JsonResponse('Item was removed', safe=False)
    elif action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'delete':
        orderItem.delete()
        return JsonResponse('Item was deleted', safe=False)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)