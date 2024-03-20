from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subsub-filtered-products/<int:id>', views.subsub_filtered_products, name='subsub-filtered-products'),
    path('featured-filtered-products', views.featured_filtered_products, name='featured-filtered-products'),
    path('category-filtered-products/<int:id>', views.category_filtered_products, name='category-filtered-products'),
    path('subcategory-filtered-products/<int:id>', views.subcategory_filtered_products, name='subcategory-filtered-products'),
    path('search-filter', views.search_filter, name='search-filter'),
    path('contact', views.contact, name='contact')
]
