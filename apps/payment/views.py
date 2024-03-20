
from django.shortcuts import render,redirect,reverse
from sslcommerz_lib import SSLCOMMERZ 
from django.views.decorators.csrf import csrf_exempt
from ..checkout.models import Order
from ..cart.models import Cart
# Create your views here.


def payment_gateway(request,track_no):
    settings = { 'store_id': 'kuber65d9c2a23469f', 'store_pass': 'kuber65d9c2a23469f@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    
    order = Order.objects.get(user=request.user,payment_status = False)
    

    status_url = request.build_absolute_uri(reverse("payment_complete"))
    post_body = {}
    post_body['total_amount'] = order.total_price
    post_body['currency'] = "BDT"
    post_body['tran_id'] = "12345"
    post_body['success_url'] = status_url
    post_body['fail_url'] = status_url
    post_body['cancel_url'] = status_url
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{order.first_name} {order.last_name}"
    post_body['cus_email'] = order.email
    post_body['cus_phone'] = order.phone
    post_body['ship_name' ] = "Madbangla"
    post_body['ship_add1' ] = order.address
    post_body['ship_city' ] = order.city
    post_body['ship_country' ] ="Bangladesh"
    post_body['ship_postcode' ] = order.postal_code
    post_body['cus_add1'] = order.address
    post_body['cus_city'] = order.city
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "YES"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Mixed"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body) #API Response

    return redirect(response['GatewayPageURL'])


@csrf_exempt
def payment_complete(request):
    if request.method=='POST' or request.method=='post':
        payment_data = request.POST
        status = payment_data['status']

        if status =="VALID":
            payment_status = "success"
            return redirect('order_page',payment_status)


        else:
            payment_status = "failure"
            return redirect('order_page',payment_status)

def order_page(request,payment_status):

    if payment_status =="success":
            neworder =  Order.objects.filter(user=request.user).order_by('-created_at').first()
            context = {
                'trackno':neworder.tracking_no,
                'total_price':neworder.total_price,
                'delivery_fee':neworder.delivery_fee,
                'ordered_items':neworder
            }
            neworder.payment_status = True
            neworder.save()
            Cart.objects.filter(user=request.user).delete()
            
            return render(request, 'order-received.html', context)

    elif payment_status == "failure":

        Order.objects.get(user=request.user,payment_status = False).delete()

        return render(request,'order-failed.html')

