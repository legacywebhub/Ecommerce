from django import forms
from .models import MyUser, ShippingDetail


class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email']



class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingDetail
        fields = ['address', 'apartment', 'city', 'state', 'country', 'zipcode', 'phone1', 'phone2']