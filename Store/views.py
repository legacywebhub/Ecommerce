from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
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
from .utils import *


'''
* Each view is seperated by 5 lines
* We have two sections: General variables section and views section
'''


# General variables

company = CompanyInfo.objects.last()
categories = Category.objects.all()
hot_products = Product.objects.filter(hot=True).order_by('?')[:3]
# Generate unique Id to use as cookie
cookie_code = generateUniqueId()



# Create your views here.

def index(request):
    new_products = Product.objects.all().order_by('-date_uploaded')[:4]
    p = Paginator(Product.objects.all(), 18)
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
            device = cookie_code
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
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
        'hot_products':hot_products,
        'new_products': new_products
    }

    # Setting up our response object
    response = render(request, 'index.html', context)
    # Using a try block to ensure there's no existing device cookie
    # before setting one
    try:
        # Checking if he already has a cookie named 'device'
        device = request.COOKIES['device']
    except:
        # If not set one using our generated cookie_code
        response.set_cookie('device', cookie_code, max_age=int(365*24*60*60))
    return response





def products(request, search):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    products_list = Product.objects.filter(name__contains=search)
    products_count = products_list.count
    p = Paginator(products_list, 18)
    page = request.GET.get('page')
    products = p.get_page(page)
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {
        'search':search,
        'products':products,
        'products_count':products_count,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'company': company,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'products.html', context)





def specialOffer(request):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    # Looping through our products and add any which percentage discount
    # is more than %15 to an empty list
    all_products = Product.objects.all()
    products_list = []
    for product in all_products:
        if product.percentage_discount > 15 and product.shipping_fee == 0:
            products_list.append(product)

    p = Paginator(products_list, 18)
    page = request.GET.get('page')
    products = p.get_page(page)
    products_count = len(products_list)
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {
        'products':products,
        'products_count':products_count,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'company': company,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'special_offers.html', context)





def category(request, category):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    products_list = Product.objects.filter(category=category)
    category = get_object_or_404(Product, id=category)
    products_count = products_list.count
    p = Paginator(products_list, 18)
    page = request.GET.get('page')
    products = p.get_page(page)
    
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {
        'company': company,
        'products':products,
        'products_count':products_count,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'category': category,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'product-category.html', context)





def cart(request):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'company': company,
        'items': order_data['items'],
        'order': order_data['order'],
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'cart.html', context)





def detail(request, pk):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
    product = get_object_or_404(Product, id=pk)
    related_products = Product.objects.filter(name__contains=product.name).order_by('?')[:6]
    
    if request.method == 'POST':
        if 'add-item-quantity' in request.POST:
            quantity = request.POST['quantity']
            orderItem, created = OrderItem.objects.get_or_create(order=order_data['order'], product=product)

            if quantity == 0:
                orderItem.delete()
            else:
                orderItem.quantity = quantity
                orderItem.save()
            return redirect('Store:cart')

            '''
            This is another way to write the code.. Either by checking the quantity first before doing
            any operation or setting quantity to order item before checking and doing operations

            orderItem.quantity = quantity

            if orderItem.quantity == 0:
                orderItem.delete()
            else:
                orderItem.save()
            ''' 
        elif 'search' in request.POST:
            search = request.POST['search']
            return redirect('/products/'+search)

    context = {
        'company': company,
        'product': product,
        'related_products': related_products,
        'item_total': order_data['item_total'],
        'total': order_data['total'],
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'product_details.html', context)





def login(request):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

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
                    
                    '''
                    Checking if the user already has a customer model before signing up
                    so we can link them rather than creating a new customer model instance
                    and can inherit the previous order before signing up
                    '''

                    try:
                        # Checking if there is a customer with device same as our cookie
                        device = request.COOKIES['device']

                        if Customer.objects.filter(device=device).exists():
                            customer = Customer.objects.get(device=device)
                            customer.user = user
                            customer.name = f'{user.first_name} {user.last_name}'
                            customer.email = user.email
                            customer.save()
                    except:
                        # Checking if there is a customer with email same as sign up email 
                            
                        if Customer.objects.filter(email=email).exists():
                            customer = Customer.objects.get(email=email)
                            customer.user = user
                            customer.save()
                        else:
                            # Create new customer if there's non
                            new_customer = Customer.objects.create(user=user, name=f'{user.first_name} {user.last_name}', email=user.email)
                            new_customer.save()

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
        elif 'search' in request.POST:
            search = request.POST['search']
            return redirect('/products/'+search)
    context = {'company': company, 'item_total': order_data['item_total'], 'total': order_data['total'], 'categories' : categories,
    'hot_products':hot_products }
    return render(request, 'login.html', context)





def logout(request):
    auth.logout(request)
    return redirect('/')





@login_required
def profile(request, user_id):
    user_instance = MyUser.objects.get(id=user_id)
    user_shipping = get_object_or_404(ShippingDetail, user=user_instance)
    # This forms here solves our bug issue after saving either of our forms
    user_form = MyUserForm(instance=user_instance)
    shipping_form = ShippingForm(instance=user_shipping)
    # Since we are sure this user is authenticated, we get the customer connected to this user directly
    customer = get_object_or_404(Customer, user=user_instance)
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
        elif 'search' in request.POST:
            search = request.POST['search']
            return redirect('/products/'+search)
    else:
        user_form = MyUserForm(instance=user_instance)
        shipping_form = ShippingForm(instance=user_shipping)

    context = {
        'company': company,
        'user_form': user_form, 
        'shipping_form': shipping_form,
        'item_total': item_total,
        'total': total,
        'categories': categories,
        'hot_products': hot_products
        }
    return render(request, 'profile.html', context)





def contact(request):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)

    if request.method == 'POST':
        if 'message' in request.POST:
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
                messages.success(request, 'Your message was sent successfully')
        elif 'search' in request.POST:
            search = request.POST['search']
            return redirect('/products/'+search)

    context = {
        'item_total': order_data['item_total'], 
        'total': order_data['total'], 
        'company': company,
        'categories': categories,
        'hot_products': hot_products
    }
    return render(request, 'contact.html', context)





def checkout(request):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'items': order_data['items'],
        'order': order_data['order'],
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'customer': order_data['customer'], 
        'company': company,
        'public_key': settings.PAYSTACK_PUBLIC_KEY,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'checkout.html', context)





def success(request, pk):
    order = Order.objects.get(id=pk)

    if not order.complete:
        messages.error(request, 'This order has not been paid for or completed')
        return redirect('/checkout/')

    items =  []
    physical = False

    # Looping through order items to get all digital products
    for item in order.orderitem_set.all():
        if item.product.digital:
            items.append(item)

    # Checking through to check if physical item for shipping
    for item in order.orderitem_set.all():
        if not item.product.digital:
            physical = True
            break

    item_total = order.item_total
    total = order.total

    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'items': items,
        'order': order,
        'item_total': item_total,
        'total': total, 
        'customer': order.customer, 
        'company': company,
        'categories' : categories,
        'hot_products':hot_products,
        'physical': physical
    }

    return render(request, 'success.html', context)

    



def faq(request):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'faq.html', context)





def legal(request):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'legal_notice.html', context)





def tac(request):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, 'tac.html', context)





def error404(request, exception):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)

    context = {
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'hot_products':hot_products
    }
    return render(request, '404.html', context)





def serverError(request):
    # Getting our customer and his order
    order_data = getCustomerAndOrder(request)
        
    if request.method == 'POST':
        search = request.POST['search']
        return redirect('/products/'+search)
    
    context = {        
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'hot_products':hot_products}
    return render(request, '500.html', context)





def newsletter(request):
    # Getting request user order
    order_data = getCustomerAndOrder(request)
    # getting all users email
    emails = MyUser.objects.all()
    # the following line of codes converts the query to a list object
    # using the read_mail function from django-pandas external module
    df = read_frame(emails, fieldnames=['email'])
    mail_list = df['email'].values.tolist()

    if request.method=="POST":
        if 'newsletter-submit' in request.POST:
            subject = request.POST['subject']
            message = request.POST['message']
            file = request.POST['file']

            if request.user.is_superuser:
                if 'file' in request.POST:
                    
                    try:
                        email = EmailMessage(subject, message, company.email1, mail_list)
                        email.content_subtype = 'html'
                        email.attach(file.name, file.read(), file.content_type)
                        email.send()
                        messages.success(request, 'Message and file succesfully sent to mail list')
                    except:
                        messages.error(request, 'Sorry... There was an error while forwarding newsletter')
                        
                else:
                    try:
                        send_mail(subject, message, company.email1, mail_list, fail_silently=False)
                        messages.success(request, 'Message succesfully sent to mail list')
                    except:
                        messages.error(request, 'Sorry... There was an error while forwarding newsletter')
            else:
                messages.error(request, 'Sorry... Only admins can forward newsletters')
        elif 'search' in request.POST:
            search = request.POST['search']
            return redirect('/products/'+search)
    
    context = {        
        'item_total': order_data['item_total'],
        'total': order_data['total'], 
        'company': company,
        'categories' : categories,
        'hot_products':hot_products,
        }
    return render(request, 'newsletter.html', context)





# Pseudo Views

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





def processShippingOrder(request):
    data = json.loads(request.body)
    print('data:', data)
    first_name = data['orderFormData']['first-name']
    last_name = data['orderFormData']['last-name']
    phone2 = data['orderFormData']['phone2']

    # Checking to see if phone2 is empty since it isn't mandactory
    # Set as None if an empty string
    if phone2 == '' or phone2 == "None":
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
        customer.email = data['orderFormData']['email']
        customer.save()
        print('customer saved')
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order.transaction_id = data['orderFormData']['transaction-id']
    total = data['orderFormData']['total']

    # Making sure total on the frontend equals total on the backend
    # Frontend may be manipulated using browser inspection tool
    if total == order.total:
        order.complete = True
    order.save()

    print('order saved')

    # Saving shipping detail for current order
    if order.shipping == True:
        shipping = Shipping.objects.create(
            customer=customer,
            order=order,
            address=data['orderFormData']['address'],
            apartment=data['orderFormData']['apartment'],
            city=data['orderFormData']['city'],
            state=data['orderFormData']['state'],
            country=data['orderFormData']['country'],
            zipcode=data['orderFormData']['zipcode'],
            phone1=data['orderFormData']['phone1'],
            phone2=phone2,
        )
        shipping.save()

    print('shipping saved')
    
    return JsonResponse('Payment and checkout was successful', safe=False)





def processNonShippingOrder(request):
    data = json.loads(request.body)
    print('data:', data)

    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        # Creating a customer using his device ID from browser
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order.transaction_id = data['orderFormData']['transaction-id']
    total = data['orderFormData']['total']

    # Making sure total on the frontend equals total on the backend
    # Frontend may be manipulated using browser inspection tool
    # Order is set to delivered because the frontend would redirect
    # to download page automatically after Json response is delivered
    if total == order.total:
        order.complete = True
        order.delivered = True
    order.save()

    print('order saved')

    return JsonResponse('Payment and checkout was successful', safe=False)