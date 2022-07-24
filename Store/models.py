from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Imports for newletter
from django.core.mail import send_mail, EmailMessage
from django_pandas.io import read_frame


# Create your models here.
class CompanyInfo(models.Model):
    logo = models.ImageField(upload_to="Images/Company", blank=True, null=True)
    name = models.CharField(max_length=150, blank=False, null=False)
    address = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=60, blank=True, null=True)
    email1 = models.EmailField(blank=False, null=False)
    email2 = models.EmailField(blank=True, null=True)
    phone1 = models.CharField(max_length=25, blank=False, null=False)
    phone2 = models.CharField(max_length=25, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    facebook_link = models.URLField(max_length=2000, blank=True, null=True)
    twitter_link = models.URLField(max_length=2000, blank=True, null=True)
    instagram_link = models.URLField(max_length=2000, blank=True, null=True)
    youtube_link = models.URLField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=60, null=False, blank=False,  help_text="e.g dollar")
    currency_shortcode = models.CharField(max_length=3, null=False, blank=False, help_text="e.g usd")
    currency_symbol = models.CharField(max_length=1, null=False, blank=False,  help_text="e.g $")
    public_key = models.CharField(max_length=160, blank=True, null=True)
    secret_key = models.CharField(max_length=160, blank=True, null=True)
    google_analytics = models.TextField(max_length=3000, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id and CompanyInfo.objects.exists():
            raise ValueError("This model cannot have two or more records")
        else:
            super().save(*args, **kwargs)


# Manager class for custom user
class MyUserManager(BaseUserManager):
    # Determines how to create our user model and validations
    def create_user(self, first_name, last_name, email, password=None):
        # Use this check for as many field you want
        if not first_name:
            raise ValueError("first name is required")
        if not last_name:
            raise ValueError("last name is required")
        if not email:
            raise ValueError("email is required")


        user = self.model(
            # normalize_email ensures our email is properly formatted
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )
        # Setting password for user
        user.set_password(password)
        # Saving user to database
        user.save(using=self._db)
        # Return user after saving
        return user

    # Determines how to create superuser
    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            password=password
        )
        # Granting permissions to the super user
        user.is_staff = True
        user.is_superuser = True
        # Saving user to database
        user.save(using=self._db)
        # Return user after saving
        return user

    '''
    Make sure to set this manager as the manager in your custom model
    objects = MyUserManager()
    '''


# Custom user model class
class MyUser(AbstractBaseUser):
    first_name = models.CharField(verbose_name="first name", max_length=60)
    last_name = models.CharField(verbose_name="last name", max_length=60)
    username = models.CharField(verbose_name="username", max_length=30, unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name="email address", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    # Setting to determing what field to use as login parameter
    USERNAME_FIELD = "email"

    # Setting to set required fields
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Setting a manager for this custom user model
    objects = MyUserManager()

    # Setting to determine what field to show on our database
    def __str__(self):
        return self.name

    # Determines if signup user has permissions
    def has_perm(self, perm, obj=None):
        return True

    # Determines if the signed up user will have acccess to other models
    # In our app or project
    def has_module_perms(self, app_label):
        return True

    '''
    Make sure to set this custom model as our user model in settings.py
    AUTH_USER_MODEL = "App.CustomUserModel"
    Make sure to delete previous migration files incase of errors
    Then make migrations
    '''

class Customer(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    device = models.CharField(max_length=25, blank=True, null=True)
    
    def __str__(self):
        if self.user:
            name = f'{self.user.first_name} {self.user.last_name}'
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


class Newsletter(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=160, blank=False, null=False)
    file = models.FileField(upload_to='Images/Newsletter', null=True, blank=True)
    body = models.TextField(max_length=5000, null=True, blank=True)
    sent_mail = models.BooleanField(default=False)

    def __str__(self):
        return(f'{str(self.date_created)}   {self.subject}')

    # Save method to send mails before saving
    # sent_mail will be False if there was an error before saving
    # sent_mail will be True if mail was sent successfully
    # remove try blocks to see errors in real time
    def save(self, *args, **kwargs):
        company = CompanyInfo.objects.last()
        users = MyUser.objects.all()

        #converts an email query to a list object
        #using the read_frame function from django-pandas external module
        df = read_frame(users, fieldnames=['email'])
        mail_list = df['email'].values.tolist()
    
        if bool(self.file) == True:
            try:
                # Checking if there is a file
                email = EmailMessage(self.subject, self.body, company.email1, mail_list)
                email.content_subtype = 'html'
                email.attach(self.file.name, self.file.read())
                email.send()
                self.sent = True
                print('Newsletter with file(s) was successfully sent to users...')
            except:
                print('Sorry... an error occured while trying to send newsletter with file(s)')
        else:
            try:
                # If there's no file
                send_mail(
                self.subject, self.body, company.email1, mail_list, fail_silently=False
                )
                self.sent = True
                print(f'Newsletter was successfully sent to users...')
            except:
                print('Sorry... an error occured while trying to send newsletter')
        # We don't intend to save newsletter images so we set file to None
        self.file = None
        super().save(*args, **kwargs)