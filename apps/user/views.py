from django.shortcuts import render, redirect
from apps.user.forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from ..checkout.models import Order, OrderItem
from ..cart.models import Cart
from ..core.utils import calculate_delivery_fee

# Create your views here.
def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful")
            return redirect('user_login')  # Redirect to 'user_login' after registration
    context = {'form': form}
    return render(request, 'register.html', context)



def user_login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('/')  # Redirect to index page after successful login
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=name, password=password)
            if user is not None:
                auth_login(request, user)
                user_cart_items = Cart.objects.filter(user = request.user)
                if not user_cart_items.exists():
                    try:
                       
                        for product_variant,item in request.session['cart_data'].items():
                                product_variant_id = product_variant
                                user_cart = Cart(
                                user = request.user,
                                product_id = product_variant_id,
                                product_quantity = int( item['quantity'])
                                )
                            
                                user_cart.save()
                        
                    except:
                        pass
                messages.success(request, "Logged in Successfully")
                return redirect('/')  # Redirect to index page after successful login
            else:
                messages.error(request, "Username or Password is incorrect")
                return render(request, 'login.html')

        return render(request, 'login.html')

    

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Logged out successfully")
        return redirect('index')
    

def user_profile(request):
    return render(request, 'user-profile.html')


def user_orders(request):
    user_orders = Order.objects.filter(user=request.user)
    context = {
        'user_orders':user_orders
    }
    return render(request, 'user-orders.html', context)

def user_order_details(request, id):
    order_products = OrderItem.objects.filter(order=id)
    order = Order.objects.get(id=id)
    delivery_fee = calculate_delivery_fee(order.city)
    
    context = {
        'order_products':order_products,
        'order':order,
        'delivery_fee':delivery_fee,
    }
    return render(request, 'user-order-details.html', context)