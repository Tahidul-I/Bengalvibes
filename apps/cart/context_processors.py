from .models import Cart

def cart_context(request):
    cart_quantity = 0
    cart_all = None
    try:
        cart_quantity = Cart.objects.filter(user=request.user).count()
        cart_all = Cart.objects.filter(user=request.user)
    except:
        pass
   
    cart_quantitiy_anonymous = 0
    cart_list_anonymous = None
    try:
        cart_quantitiy_anonymous = len((request.session['cart_data']))
        cart_list_anonymous = request.session['cart_data']
    except:
        pass
    return{
        'cart_all':cart_all,
        'cart_quantity':cart_quantity,
        'cart_list_anonymous':cart_list_anonymous,
        'cart_quantitiy_anonymous':cart_quantitiy_anonymous
    }