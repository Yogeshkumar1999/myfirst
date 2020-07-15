from django.forms import ModelForm
#django has inbulilt forms
from django.contrib.auth.forms import UserCreationForm
from .models import Order, Customer, Product
from django import forms
from django.contrib.auth.models import User


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fileds = '__all__'
        exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
