from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.models import auth
from .forms import MyUserForm, ShippingForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .utils import generateUniqueId


# General variables

company = CompanyInfo.objects.last()
categories = Category.objects.all()
hot_products = Product.objects.filter(hot=True).order_by('?')[:3]


# Create your views here.

def index(request):
    p = Paginator(Product.objects.all(), 3)
    page = request.GET.get('page')
    products = p.get_page(page)

    # Generate unique Id to use as cookie
    cookie_code = generateUniqueId()
    
    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        try:
            # Try getting a customer using his device ID from browser
            device = request.COOKIES['device']
        except:
            device = cookie_code
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items =  order.orderitem_set.all()
    item_total = order.item_total
    total = order.total


    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'company': company,
        'products': products,
        'item_total': item_total,
        'total': total,
        'categories' : categories,
        'hot_products':hot_products
    }
    response = render(request, 'index.html', context)
    # Setting the generated cookie_code for our response
    response.set_cookie('device', cookie_code)
    return response


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
        try:
            # Try getting a customer using his device ID from browser
            device = request.COOKIES['device']
        except:
            # Redirect to index page to set a cookie for request user
            return redirect('/')
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
        'company': company,
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
        try:
            # Try getting a customer using his device ID from browser
            device = request.COOKIES['device']
        except:
            # Redirect to index page to set a cookie for request user
            return redirect('/')
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    item_total = order.item_total
    total = order.total
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {
        'company': company,
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
        try:
            # Try getting a customer using his device ID from browser
            device = request.COOKIES['device']
        except:
            # Redirect to index page to set a cookie for request user
            return redirect('/')
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items =  order.orderitem_set.all()
    item_total = order.item_total
    total = order.total
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'company': company,
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
        try:
            # Try getting a customer using his device ID from browser
            device = request.COOKIES['device']
        except:
            # Redirect to index page to set a cookie for request user
            return redirect('/')
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    item_total = order.item_total
    total = order.total
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    context = {
        'company': company,
        'product': product,
        'item_total': item_total,
        'total':total,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'product_details.html', context)



def login(request):
    if request.method == "POST":
        if 'register-submit' in request.POST:
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            email = request.POST['register-email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password2 == password1:
                if MyUser.objects.filter(email=email).exists():
                    messages.error(request, 'Sorry this email has already been taken!')
                else:
                    # Saving user and user instances
                    user = MyUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password2)
                    user.save()
                    customer = Customer.objects.create(user=user, name=f'{user.first_name} {user.last_name}', email=user.email)
                    customer.save()
                    user_shipping_detail = ShippingDetail.objects.create(user=user)
                    user_shipping_detail.save()
                    messages.success(request, 'Your account has successfully been created... you can now sign in!')
            else:
                messages.error(request, 'Passwords does not match... Please try again')   
        elif 'login-submit' in request.POST:
            email = request.POST['login-email']
            password = request.POST['password']

            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid credentials..   Please try again')
    context = {'company': company,}
    return render(request, 'login.html', context)



def logout(request):
    auth.logout(request)
    return redirect('/')



@login_required
def profile(request, user_id):
    user_instance = MyUser.objects.get(id=user_id)
    user_shipping = ShippingDetail.objects.get(user=user_instance)
    # This forms here solves our bug issue after saving either of our forms
    user_form = MyUserForm(instance=user_instance)
    shipping_form = ShippingForm(instance=user_shipping)
    # Since we are sure this user is authenticated, we get the customer connect to this user directly
    customer = Customer.objects.get(user=user_instance)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    item_total = order.item_total
    total = order.total

    if request.method == "POST":
        if 'save-user-detail' in request.POST:
            user_form = MyUserForm(request.POST or None, instance=user_instance)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'profile successfully updated')
        elif 'save-shipping-detail' in request.POST:
            shipping_form = ShippingForm(request.POST or None, instance=user_shipping)
            if shipping_form.is_valid():
                shipping_form.save()
                messages.success(request, 'shipping details successfully updated')
    else:
        user_form = MyUserForm(instance=user_instance)
        shipping_form = ShippingForm(instance=user_shipping)
    context = {
        'company': company,
        'user_form': user_form, 
        'shipping_form': shipping_form,
        'item_total': item_total,
        'total': total
        }
    return render(request, 'profile.html', context)



def contact(request):
    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        try:
            # Try getting a customer using his device ID from browser
            device = request.COOKIES['device']
        except:
            # Redirect to index page to set a cookie for request user
            return redirect('/')
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
                try:
                    # Trying to notify company or admins via mail
                    send_mail(
                    f'{subject}({location})', message, email, [company.email1, company.email2], fail_silently=False
                    )
                    print(f'Message was successfully sent to admins...')
                except:
                    pass
                message = Message.objects.create(name=name, location=location, email=email, subject=subject, message=message)
                message.save()
                messages.info(request, 'Your message was sent successfully')
                return redirect('Store:contact')

    context = {'item_total':item_total, 'total':total, 'company': company,}
    return render(request, 'contact.html', context)

def checkout(request):
    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        try:
            # Try getting a customer using his device ID from browser
            device = request.COOKIES['device']
        except:
            # Redirect to index page to set a cookie for request user
            return redirect('/')
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items =  order.orderitem_set.all()
    item_total = order.item_total
    total = order.total

    context = {
        'company': company,
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
        shipping_details = Shipping.objects.create(
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