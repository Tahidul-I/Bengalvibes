from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import random
from .models import Order, OrderItem
from ..cart.models import Cart
from ..products.models import ProductVariation
from ..core.utils import calculate_delivery_fee

# Create your views here.
@login_required(login_url='user_login')
def checkout(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_quantity > item.product_quantity:
            Cart.objects.delete(id=item.id)
    
    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0

    for item in cart_items:
        total_price = total_price +  item.product.selling_price * item.product_quantity

    context = {
        'cart_items':cart_items,
        'total_price':total_price
    }
    return render(request, 'checkout.html', context)


@login_required(login_url='user_login')
def placeorder(request):
    if request.method == 'POST':
        try:
            existing_order = Order.objects.get(user=request.user,payment_status=False)
            existing_order.delete()
        except:
            pass
        neworder = Order()
        neworder.user = request.user
        neworder.first_name = request.POST.get('first_name')
        neworder.last_name = request.POST.get('last_name')
        neworder.city = request.POST.get('city')

        delivery_fee = calculate_delivery_fee(neworder.city)
        neworder.delivery_fee = delivery_fee
        neworder.address = request.POST.get('address')
        neworder.postal_code = request.POST.get('postal_code')
        neworder.phone = request.POST.get('phone')
        neworder.email = request.POST.get('email')
        neworder.message = request.POST.get('message')
        neworder.payment_mode = request.POST.get('payment_mode')
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.product_quantity

        neworder.total_price = cart_total_price + delivery_fee

        trackno = 'rarepro'+str(random.randint(111111,999999))

        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'rarepro'+str(random.randint(111111,999999))
        
        neworder.tracking_no = trackno
        neworder.save()
        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                product = item.product,
                price = item.product.selling_price,
                quantity = item.product_quantity
            )
            orderproduct = ProductVariation.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_quantity

            orderproduct.save()

        
        if request.POST.get('payment_mode') == "PO":

            return redirect('payment_gateway',neworder.tracking_no)
        
        if request.POST.get('payment_mode') == "COD":
            payment_status = "success"

            return redirect('order_page',payment_status)
            
    return redirect('index')