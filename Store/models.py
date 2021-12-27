from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    color = (
        ('black', 'black'),
        ('red', 'red'),
        ('white', 'white'),
        ('yellow', 'yellow'),
        ('purple', 'purple'),
        ('green', 'green'),
        ('blue', 'blue'),
        ('others', 'others'),
    )
    category = (
        ('clothing', 'clothing'),
        ('shoes', 'shoes'),
        ('electronics', 'electronics'),
        ('accessories', 'accessories'),
    )
    category = models.CharField(max_length=50, choices=category, default='electronics')
    name = models.CharField(max_length=200, null=False, blank=False)
    brand = models.CharField(max_length=200, null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    image1 = models.ImageField(upload_to='Images/Products',blank=False, null=False)
    image2 = models.ImageField(upload_to='Images/Products',blank=True, null=True)
    image3 = models.ImageField(upload_to='Images/Products',blank=True, null=True)
    image_url1 = models.CharField(max_length=3000, blank=True, null=True)
    image_url2 = models.CharField(max_length=3000, blank=True, null=True)
    image_url3 = models.CharField(max_length=3000, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, choices=color, default='black')
    weight = models.CharField(max_length=50, blank=True, null=True)
    digital = models.BooleanField(default=False, null=False, blank=False)
    description = models.TextField(max_length=3000, null=True, blank=False)
    date_released = models.DateField(blank=True, null=True)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    hot = models.BooleanField(default=True, null=False, blank=False)
    new = models.BooleanField(default=True, null=False, blank=False) 
    available = models.BooleanField(default=True, null=False, blank=False)
    
    def __str__(self):
        return self.name
    
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
    
    def __str__(self):
        return str(self.id)
    
    @property
    def cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.price_total for item in orderitems])
        return  total
    
    @property
    def discount_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.product.discount for item in orderitems])
        return total
    
    @property
    def tax_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.product.tax for item in orderitems])
        return total
    
    @property
    def item_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return  total
    
    @property
    def total(self):
        total = self.cart_total - (self.discount_total + self.tax_total)
        return total
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name
    
    @property
    def price_total(self):
        total = self.product.price * self.quantity
        return total
    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=False, blank=False)
    city = models.CharField(max_length=200, null=False, blank=False)
    state = models.CharField(max_length=200, null=False, blank=False)
    zipcode = models.CharField(max_length=200, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    
class Message(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    location = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    subject = models.CharField(max_length=100, null=False, blank=False)
    message = models.TextField(max_length=3000, null=False, blank=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.date_sent