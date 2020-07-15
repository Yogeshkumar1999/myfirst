from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
#To get the default usercreation form.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

#create multiple form
from .models import *
#custoomsied user creation form.
from .forms import OrderForm, CreateUserForm, CustomerForm, ProductForm
from .filters import OrderFilter, ProductFilter
from .decorators import unauthenticated_user, allowed_users, admin_only



@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+username)
            return redirect('login')
    context = {'form':form}
    print("ok1")
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username Or password is incorrect')
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    customer = request.user.customer
    orders_count = orders.count()
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    myFilter = OrderFilter(request.GET, queryset = orders)
    orders = myFilter.qs
    context = {'customer':customer, 'orders': orders, 'orders_count':orders_count, 'myFilter':myFilter, \
            'total_orders':total_orders, 'delivered': delivered, 'pending':pending}
    return  render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    print(request.user.customer.profile_pic.url)
    form = CustomerForm(instance = customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = customer)
        if form.is_valid:
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@admin_only
def customersData(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    context = {'customers':customers, 'orders':orders}
    return render(request, 'accounts/customers_data.html', context)


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    orders = orders[:5]
    customers = customers[:5]
    context = {'orders': orders, 'customers': customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset = products)
    products = myFilter.qs
    context = {'products':products, 'myFilter':myFilter}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    myFilter = OrderFilter(request.GET, queryset = orders)
    orders = myFilter.qs
    context = {'customer':customer, 'orders': orders, 'orders_count':total_orders, 'myFilter':myFilter, 'total_orders':total_orders, \
                        'delivered':delivered, 'pending':pending}
    return  render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product',))
    customer = Customer.objects.get(id=pk)
    #In the OrderForm we send the customer to auto fill the customer field
    #form = OrderForm(initial={'customer':customer})
    #(queryset = Order.objects.none() to avoid showing the already exixts orders.
    formset = OrderFormSet(queryset = Order.objects.none(), instance=customer)
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    print(order)
    form = OrderForm(instance=order)
    print(form)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/update_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid:
            form.save()
            return redirect('products')
    context = {'form': form}
    return render(request, 'accounts/update_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
            product.delete()
            return redirect('products')

    context = {'item': product}
    return render(request, 'accounts/delete_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addProducts(request):
    form = ProductForm()
    if request.method == 'POST':
        print(form)
        form = ProductForm(request.POST)
        print(form)
        if form.is_valid:
            form.save()
            return redirect('products')

    context = {'form':form}
    return render(request, 'accounts/add_products.html', context)

