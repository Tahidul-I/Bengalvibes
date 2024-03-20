from .models import Category

def category_context(request):
    category_all = Category.objects.all()
    featured_category_all = Category.objects.filter(is_featured=True)
    return{
        'category_all':category_all,
        'featured_category_all':featured_category_all
    }