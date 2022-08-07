from django.contrib import admin
from .models import *
from django.utils.html import format_html


# Admin Classes
class CompanyInfoAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('name', 'logo', 'currency')

    def logo(self, obj):
        if obj.logo:
            logo = format_html(f'<img src="/media/{obj.logo}" style="width:100px;">')
        else:
            logo = ''
        return logo



class MyUserAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('name', 'email')
    list_per_page = 30



class CustomerAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('name', 'device', 'email')
    list_per_page = 20



class ShippingDetailAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('__str__', 'country',)
    list_per_page = 30



class ProductAdmin(admin.ModelAdmin):
    exclude = ('date_uploaded',)
    list_display = ('name', 'category', 'product_image', 'price', 'percentage_discount')
    list_filter = ('category', 'available', 'digital', 'date_uploaded',)
    list_per_page = 20

    def product_image(self, obj):
        if obj.image1:
            image = format_html(f'<img src="/media/{obj.image1}" style="width:100px;">')
        elif obj.image_url1:
            image = format_html(f'<img src="{obj.image_url1}" style="width:100px;">')
        else:
            image = ''
        return image



class OrderAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('id', 'customer_name', 'complete', 'delivered',)
    list_filter = ('date_ordered', 'complete', 'delivered',)
    list_per_page = 20



class ShippingAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('customer_name', 'order', 'country')
    list_filter = ('date_added',)
    list_per_page = 20



class MessageAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('name', 'location', 'subject', 'email')
    list_filter = ('date_received',)
    list_per_page = 20



class NewsletterAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('date_created', 'subject',)
    list_filter = ('date_created', 'sent_mail',)
    list_per_page = 20



class OrderItemAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('__str__', 'order', 'quantity')
    list_filter = ('date_added',)
    list_per_page = 30



# Register your models here.
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(ShippingDetail, ShippingDetailAdmin)
admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Message, MessageAdmin)