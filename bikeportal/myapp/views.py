from email import message
from unicodedata import category
from cart.cart import Cart
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import mail_admins
from django.core.mail import send_mail as sm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from myapp.Order_id.orderid import generate_id

from .forms import Registration
from .models import ( Product, Rating, Shop,
                     mechanic, order_detail)



def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    quanty = request.POST.get('qty')
    print("----------->q",quanty)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url='login')
def cart_detail(request):
    return render(request, 'myapp/cart.html')


# Create your views here.
def home(request):    
    return render(request, 'myapp/index.html')


def about(request):
    return render(request, 'myapp/about.html')

def product(request):
    get_val = request.GET.get('val', None)
    if get_val:
        product = Product.objects.filter(category=get_val)
        return render(request, 'myapp/product.html',{'products':product})
    product = Product.objects.all()
    return render(request, 'myapp/product.html',{'products':product})

def services(request):
    return render(request, 'myapp/order_msg.html')

@csrf_exempt
def detail(request, id):
    selected_product = Product.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        rat = Rating(name = name, email=email, rating=rating, review = review, user= request.user, product=selected_product)
        # instance = rat.save()
        # instance.user = request.user
        rat.save()
        return messages.success("Thanks to rate us our product!")
    print(id)
    rating = Rating.objects.filter(product=selected_product.id)
    print(selected_product.name)
    return render(request, 'myapp/detail.html',{'selected_product': selected_product,'rating':rating})

@login_required(login_url='login')
def cart(request):
    total= 0
    cart = Cart(request)
    print("---------->",request.session['cart'])
    if cart:
        for key, value in request.session['cart'].items():
            total = total + (float(value['price']) * value['quantity'])
    else:
        total = 0.0    
    request.session['t_total'] = total
    return render(request, 'myapp/cart.html')

@csrf_exempt
def checkout(request):
    items = request.session.get('cart')
    total_price = request.session.get('t_total')
    order_id = generate_id()
    
    if request.method=='POST':
        first_name=request.POST.get('first_name',None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        phone_number = request.POST.get('phone', None)
        city = request.POST.get('city', None)
        zip_code = request.POST.get('zip')
        address = request.POST.get('address')
        delivery_inststruction = request.POST.get('instruction')
#         subject = 'Online Shopping'
#         mes = f'Hi {first_name} your Order against {order_id} has been submitted. You can track order status by entering the id in our portal.'    
#         sm(subject, mes,'f2018105044@umt.edu.pk',[email], fail_silently=True)
#         messages.success(request, f'Your Order against {order_id} has been successfully added. Thanks to become our valuable customer!!')
#         mail_admins(
#              'Order',
#      f'A new order has been submited with id {order_id}.',
#      fail_silently=True
#  ) 
        order = order_detail(order_id = order_id,items = items,total = total_price, first_name=first_name, last_name=last_name, email=email,
        phone_number = phone_number, zip_code=zip_code, city=city, address=address,delivery_instruction= delivery_inststruction, user=request.user)
        instance = order.save()
        order.send_mail(email,{'cart':items,'total_p':total_price})
        Product.update_quantity()
        cart = Cart(request)
        cart.clear()
        return HttpResponse(f'Your Order against {order_id} has been successfully added. Thanks to become our valuable customer!!')

    return render(request, 'myapp/checkout.html')


def contact(request):
    cart = Cart(request)
    print(cart['id'])
    return render(request, 'myapp/contact.html')

def Mechanic(request):
    location = mechanic.objects.all()
    name = []
    # for i in location:
    #     name.append('name' : i.area_name)
    # print(name)
    location = serializers.serialize('json', location)
    print(location)
    return render(request, 'myapp/mechanic.html' , {'locations':location})


def signup(request):
    if request.method=='POST':
        form=Registration(request.POST)
        if form.is_valid():
            messages.success(request,' Account has been successfully created you can now login!')
            form.save()
            return redirect('/home/login/')
    else:
        form=Registration
    return render(request,"myapp/signup.html",{'form':form})

# login view
def user_login(request):
    if request.method == 'POST':
        form=AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            passw = form.cleaned_data['password']
            user = authenticate(username=uname, password=passw)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {uname}")
                return redirect('/home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form':form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/home/login/')
