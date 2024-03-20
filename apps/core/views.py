from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from ..category.models import *
from ..advertisement.models import Banner, VerticalBannerProudctAdvertisement, VerticalBannerAdvertisement
from ..products.models import Product
from .models import SiteInfo
from ..advertisement.models import VideoAdvertisement
# Create your views here.
def index(request):
    category_all = Category.objects.all()
    subcategory_all = SubCategory.objects.all()
    subsubcategory_all = SubSubCategory.objects.all()
    banner_all = Banner.objects.all()
    featured_products_all = Product.objects.filter(is_featured = True).order_by('?')[:6]
    new_arrival_products_all = Product.objects.filter(new_arrival = True).order_by('?')[:6]
    best_seller_products_all = Product.objects.filter(new_arrival = True).order_by('?')[:6]
    featured_category_all = Category.objects.filter(is_featured=True)
    video_advertisement = VideoAdvertisement.objects.first()

    vertical_banner_product_advertisement_1 = VerticalBannerProudctAdvertisement.objects.all()[:1]
    vertical_banner_advertisement_products_1 = Product.objects.filter(vertical_banners_product__in=vertical_banner_product_advertisement_1)[:6]
    vertical_banner_product_advertisement_2 = VerticalBannerProudctAdvertisement.objects.all()[1:2]
    vertical_banner_advertisement_products_2 = Product.objects.filter(vertical_banners_product__in=vertical_banner_product_advertisement_2)[:6]

    vertical_banner_advertisement_all = VerticalBannerAdvertisement.objects.all()[:3]
    # Collect products related to all VerticalBannerProudctAdvertisement instances

    
    context = {
        'category_all':category_all, 
        'banner_all':banner_all, 
        'featured_products_all':featured_products_all, 
        'subcategory_all':subcategory_all, 
        'subsubcategory_all':subsubcategory_all, 
        'featured_category_all':featured_category_all,
        'video_advertisement':video_advertisement,

        'vertical_banner_product_advertisement_1':vertical_banner_product_advertisement_1,
        'vertical_banner_advertisement_products_1':vertical_banner_advertisement_products_1,
        'vertical_banner_advertisement_products_2':vertical_banner_advertisement_products_2,
        'vertical_banner_product_advertisement_2':vertical_banner_product_advertisement_2,

        'best_seller_products_all':best_seller_products_all,

        'vertical_banner_advertisement_all':vertical_banner_advertisement_all,
        'new_arrival_products_all':new_arrival_products_all
        }
    return render(request, 'index.html', context)


def filtered_products(request, banner_image=None, **kwargs):
    """
    Generic function to filter products based on given parameters and render the template.
    """
    products =None
    try:
        products = Product.objects.filter(**kwargs)
    except:
        pass
    
    context = {'filtered_products': products, 'banner_image': banner_image}
    return render(request, "filtered-products.html", context)

def subsub_filtered_products(request, id):
    subsubcategory = SubSubCategory.objects.get(id=id)
    print(subsubcategory.title)
   

    # Add banner_image as needed for subsub_filtered_products
    banner_image = subsubcategory.subcategory.category.banner.url if subsubcategory.subcategory.category.banner else None

    return filtered_products(request, banner_image=banner_image, subsubcategory_tag=subsubcategory)


def featured_filtered_products(request):
    # Get the SiteInfo instance (assuming there's only one instance)
    site_info = SiteInfo.get_site_info()

    # Access the 'featured_banner' field from SiteInfo
    banner_image = site_info.featured_banner.url if site_info.featured_banner else None

    return filtered_products(request,banner_image=banner_image, is_featured=True)


def category_filtered_products(request, id):
    category = Category.objects.get(id=id)
    # Get the banner image from the Category model
    banner_image = category.banner.url if category.banner else None
    return filtered_products(request,banner_image=banner_image, subcategory__category=category)

def subcategory_filtered_products(request, id):
    
    subcategory = SubCategory.objects.get(id=id)
    # Get the banner image from the Category model
    banner_image = subcategory.category.banner.url if subcategory.category.banner else None
    return filtered_products(request,banner_image=banner_image, subcategory=subcategory)


def contact(request):
    return render(request, 'contact.html')


def search_filter(request):
    if request.method == "POST":
        tag = request.POST.get('tag')
        # Store the tag in the session to preserve it across the redirect
        request.session['search_tag'] = tag
        # Redirect to the same page to avoid form resubmission
        return HttpResponseRedirect(request.path_info)

    # If it's a GET request, retrieve the search tag from the session (if available)
    tag = request.session.get('search_tag')
    if tag:
        # If a search tag is found in the session, perform the search
        filtered_products_all = Product.objects.filter(tag__title=tag)
    else:
        # If no search tag is found, redirect to the index page or handle it as needed
        return redirect('index')

    # Render the template with the filtered products
    return render(request, 'search-filtered-products.html', {'filtered_products_all': filtered_products_all})
