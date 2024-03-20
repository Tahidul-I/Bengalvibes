from django.http import JsonResponse
from django.shortcuts import redirect, render
from ..products.models import ProductVariation
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import Cart
# Create your views here.
from django.http import JsonResponse
import json

def add_to_cart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            color_id = int(request.POST.get('color_id'))
            size_id = int(request.POST.get('size_id'))
            product_quantity = int(request.POST.get('product_quantity'))
            product_check = ProductVariation.objects.filter(product_id=product_id, color=color_id, size=size_id).first()
            if product_check:
                user_cart_item = Cart.objects.filter(user=request.user, product_id=product_check.id).first()

                if user_cart_item:
                    check_quantity = user_cart_item.product_quantity + product_quantity
                    print(check_quantity)
                    if check_quantity <= product_check.quantity:
                    # If the product is already in the cart, increment the quantity
                        product_quantity = int(request.POST.get('product_quantity'))
                        new_quantity = user_cart_item.product_quantity + product_quantity
                        user_cart_item.product_quantity = new_quantity
                        user_cart_item.save()

                        return JsonResponse({'success_status': f'Quantity updated to {new_quantity}'})

                    else:
                        return JsonResponse({'error_status': f'Only {product_check.quantity} pieces available' })

                else:
                    # If the product is not in the cart, add it
                    

                    if product_check.quantity >= product_quantity:
                        print("*************************** NEW AVILABLE************************************")
                        Cart.objects.create(user=request.user, product_id=product_check.id, product_quantity=product_quantity)
                        total_cart_quantity = Cart.objects.filter(user=request.user).count()
                        return JsonResponse({'success_status': "Product added successfully",'total_cart_quantity':total_cart_quantity})
                    else:
                        print("*************************** NEW NOT AVILABLE************************************")
                        return JsonResponse({'error_status': f'Only {product_check.quantity} pieces available'})
            else:
                return JsonResponse({'warning_status': 'No such product found'})


    return redirect('index')


def cart(request):
    if request.user.is_anonymous:
        cart_list = None
        try:
            cart_list = request.session['cart_data']

        except:
            pass

        if cart_list is not None:
            context = {
                'cart_list':cart_list
            }
            return render(request, 'cart.html',context)
        else:
            return render(request, 'empty_cart.html')
    
    if request.user.is_authenticated:
        
        user_cart = None
        try:
            user_cart = Cart.objects.filter(user=request.user).first()
           
        except:
           pass

        if user_cart is not None:
            return render(request, 'cart.html')
        else:
            return render(request, 'empty_cart.html')

        
def update_cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            product_id = int(request.POST.get('product_id'))
            print(product_id)
            if(Cart.objects.filter(user=request.user, product_id=product_id)):
                cart = Cart.objects.get(product_id=product_id, user= request.user)
                cart.product_quantity = int(request.POST.get('product_quantity'))
                cart.save()
                user_cart = Cart.objects.filter(user=request.user)
                context = {
                    'user_cart':user_cart
                }
                update_cart_template = render_to_string("ajax/update_cart_authenticated.html",context)

                return JsonResponse({'status':'Updated Successfully','update_cart_template':update_cart_template})
            else:
                return JsonResponse({'error':'Item does not exist in the cart'})
        return redirect('index')

    if request.user.is_anonymous:
        
        if request.method == 'POST':
            product_variant_id =  int(request.POST.get('product_variant_id'))
            product_quantity = int(request.POST.get('product_quantity'))
            cartdata = request.session['cart_data']
            cartdata[f"{product_variant_id}"]['quantity'] = product_quantity 
            request.session['cart_data'] = cartdata
            cart_list = request.session['cart_data']
            context={
                'cart_list':cart_list
            }
            update_cart_template = render_to_string("ajax/update_cart_anonymous.html",context)
            return JsonResponse({'status':'Updated Successfully','update_cart_template':update_cart_template})
           
        return redirect('index')

def delete_cart_item(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            product_id = int(request.POST.get('product_id'))
            section_count = int(request.POST.get('section_count'))
            selected_cart_product = Cart.objects.get(product_id=product_id, user=request.user)
            selected_cart_product.delete()
            total_cart_quantity = Cart.objects.filter(user=request.user).count()
            print(total_cart_quantity)
            # if(Cart.objects.filter(user=request.user, product_id=product_id)):
            #     cartitem = Cart.objects.get(product_id=product_id, user=request.user)
            #     cartitem.delete()
            if section_count == 1:
                message = '<h1>Your Cart Is Empty</h1>'
                return JsonResponse({'message':message,'total_cart_quantity':total_cart_quantity})
            else:

                return JsonResponse({'status':'Deleted successfully','total_cart_quantity':total_cart_quantity})

        return redirect('index')
    if request.user.is_anonymous:
        if request.method =='POST':
            product_variant_id = request.POST.get('product_id')
            section_count = int(request.POST.get('section_count'))
            cart_list = request.session['cart_data']
            del cart_list[product_variant_id]
            request.session['cart_data']=cart_list
            total_cart_quantity = len( request.session['cart_data'])
            if section_count == 1:
                del request.session['cart_data']
                message = '<h1>Your Cart Is Empty</h1>'
                return JsonResponse({'message':message,'total_cart_quantity':total_cart_quantity})
            else:

                return JsonResponse({'status':'Deleted successfully','total_cart_quantity':total_cart_quantity})

        return redirect('index')




def add_to_cart_anonymous(request):
    
    json_data = json.loads(request.body.decode('utf-8'))
    product_id = int(json_data.get('product_id'))
    product_color_id = int(json_data.get('color_id'))
    product_size_id = int(json_data.get('size_id'))
    product_price= int(json_data.get('product_price'))
    product_quantity= int(json_data.get('product_quantity'))
    product_image = json_data.get('product_image')
    product_variant = ProductVariation.objects.get(size_id = product_size_id, color_id = product_color_id, product_id = product_id)

    cart = {}
    cart[str(product_variant.id)]={
        'title':f"{product_variant.product.title}" ,
        'price':product_price,
        'slug':f"{product_variant.product.slug}",
        'quantity': product_quantity,
        'color': f"{product_variant.color.title}",
        'size':  f"{product_variant.size.title}",
        'stock_quantity': product_variant.quantity,
        'image': product_image
    }
    
    if 'cart_data' in request.session:

            # Updating product quantity in session cart_data if the product already exist

        if str(product_variant.id) in request.session['cart_data']:
            cartdata =  request.session['cart_data']
            updated_quantity = int(cartdata[str(product_variant.id)]['quantity'])+int(json_data.get('product_quantity'))
            if updated_quantity <= product_variant.quantity:
                cartdata[str(product_variant.id)]['quantity'] = updated_quantity
                cartdata.update(cartdata)
                request.session['cart_data']=cartdata
                cart_list = request.session['cart_data']
                context={
                    'cart_list':cart_list
                }

                # template = render_to_string('ajax/product_details_anonymous_user.html',context)
                message = f"Quantity updated to { cartdata[str(product_variant.id)]['quantity']}"
                return JsonResponse({'total_cart_items':len(request.session['cart_data']),'success_status':message})
            else:
                return JsonResponse({'error_status':f"Only {product_variant.quantity} pieces available"})
        
        # Adding new product in session cart_data
            
        else:
            if product_quantity <= product_variant.quantity:
                cartdata = request.session['cart_data']
                cartdata.update(cart)
                request.session['cart_data']=cartdata
                cart_list = request.session['cart_data']
                context={
                    'cart_list':cart_list
                }

                # template = render_to_string('ajax/product_details_anonymous_user.html',context)

                return JsonResponse({'total_cart_items':len(request.session['cart_data']),'success_status': "Product added successfully"})
            else:

                return JsonResponse({'error_status':f"Only {product_variant.quantity} pieces available"})
            
        # Creating the session cart_data if not creaeted

    else:

        if product_quantity <= product_variant.quantity:

            request.session['cart_data'] = cart
            cart_list = request.session['cart_data']
            context={
                'cart_list':cart_list
            }
            
            # template = render_to_string('ajax/product_details_anonymous_user.html',context)
            return JsonResponse({'total_cart_items':len(request.session['cart_data']),'success_status': "Product added successfully"})

        else:

            return JsonResponse({'error_status':f"Only {product_variant.quantity} pieces available"})
    
def delete_cart_all_item(request):

    if request.user.is_authenticated:
        user_cart = Cart.objects.filter(user=request.user)
        user_cart.delete()
        return render(request,'empty_cart.html')
    
    if request.user.is_anonymous:
        del request.session['cart_data']
        return render(request,'empty_cart.html')