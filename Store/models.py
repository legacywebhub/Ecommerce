from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    device = models.CharField(max_length=25, blank=True, null=True)
    
    def __str__(self):
        if self.user:
            name = f'{self.user.first_name} {self.user.last_name}' or self.user.username
        elif self.name:
            name = self.name
        else:
            name = self.device
        return str(name)


class Category(models.Model):
    category = models.CharField(max_length=60, unique=True, blank=True, null=False)

    def __str__(self):
        return self.category


class ProductCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    product_category = models.CharField(max_length=60, unique=True, blank=False, null=False)

    def __str__(self):
        return self.product_category

    
class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    brand = models.CharField(max_length=200, null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    image1 = models.ImageField(upload_to='Images/Products',blank=False, null=False)
    image2 = models.ImageField(upload_to='Images/Products',blank=True, null=True)
    image3 = models.ImageField(upload_to='Images/Products',blank=True, null=True)
    image_url1 = models.URLField(max_length=3000, blank=True, null=True)
    image_url2 = models.URLField(max_length=3000, blank=True, null=True)
    image_url3 = models.URLField(max_length=3000, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    weight = models.CharField(max_length=50, blank=True, null=True)
    digital = models.BooleanField(default=False, null=False, blank=False)
    description = models.TextField(max_length=3000, null=True, blank=False)
    date_released = models.DateField(blank=True, null=True)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    shipping_fee = models.FloatField(default=0)
    hot = models.BooleanField(default=True, null=False, blank=False)
    new = models.BooleanField(default=True, null=False, blank=False) 
    available = models.BooleanField(default=True, null=False, blank=False)
    
    # __str__ function determines what field to represent on the admin dashboard
    def __str__(self):
        return self.name
    

    # Function to fix application crash if we don't have an image
    # This can also be fixed on our frontend by using if statement to check
    # if we have an image and then render something else if we dont have
    @property
    def image2URL(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    
    @property
    def image3URL(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url
    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    delivered = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)

    # Function to sum up prices for all order items in our cart 
    @property
    def price_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.item_price_total for item in orderitems])
        return  total
    
    # Function to sum up discount for all order items in our cart
    @property
    def discount_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.product.discount for item in orderitems])
        return total
    
    # Function to sum up tax for all order items in our cart
    @property
    def tax_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.product.tax for item in orderitems])
        return total

    # Function to sum up shipping fee for all order items in our cart
    @property
    def shipping_fee_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.product.shipping_fee for item in orderitems])
        return total
    
    # Function to sum up total order items in our cart and reset when order is delivered
    @property
    def item_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        # Resetting order items after delivery or delivered status has been set to true
        if self.delivered == True:
            for i in orderitems:
                i.quantity = 0
                total = i.quantity
        return  total
    
    # Function to calculate total bill of customer using other functions
    @property
    def total(self):
        total = (self.price_total + self.shipping_fee_total + self.tax_total) - self.discount_total
        return total
    
    # Function to loop through our products to check if there is a physical product for shipping
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name
    
    # Function to calculate price of item by it's quantity
    @property
    def item_price_total(self):
        total = self.product.price * self.quantity
        return total
    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=False, blank=False)
    apartment = models.CharField(max_length=200, null=False, blank=False, default='apartment')
    city = models.CharField(max_length=200, null=False, blank=False)
    state = models.CharField(max_length=200, null=False, blank=False)
    country = models.CharField(max_length=200, null=False, blank=False)
    zipcode = models.CharField(max_length=200, null=False, blank=False)
    phone1 = models.IntegerField(null=False, blank=False)
    phone2 = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.customer.name} {self.address}'
    
class Message(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    location = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    subject = models.CharField(max_length=100, null=False, blank=False)
    message = models.TextField(max_length=3000, null=False, blank=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.date_sent}'