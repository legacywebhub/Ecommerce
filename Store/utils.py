from datetime import datetime
from django.shortcuts import render, redirect
from .models import *


# Functions

# Generating a unique code used as order or transaction id
# Or cookie to identify unique customers
def generateUniqueId():
    return str(datetime.now().timestamp()).replace('.', '-')

# View functions for D.R.Y principle
def getCustomerAndOrder(request):
    try:
        # Trying to get customer from authenticated user
        customer = request.user.customer
    except:
        try:
            # Try getting a customer using his device ID from browser
            device = request.COOKIES['device']
        except:
            # Redirect to index page to set a cookie for request user
            # if there's an error or no cookie
            return redirect('/')
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items =  order.orderitem_set.all()
    item_total = order.item_total
    total = order.total

    return {'items':items, 'order':order, 'item_total': item_total, 'total': total, 'customer': customer,}


