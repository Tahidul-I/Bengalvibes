from django.urls import path
from . import views
urlpatterns = [
    path('add-to-cart', views.add_to_cart, name="add-to-cart"),
    path('add-to-cart-anonymous/', views.add_to_cart_anonymous, name="add-to-cart-anonymous"),
    path('cart-details', views.cart, name="cart"),
    path('update-cart', views.update_cart, name="update-cart"),
    path('delete-cart-item', views.delete_cart_item, name="delete-cart-item"),
    path('delete-cart-all-item', views.delete_cart_all_item, name="delete-cart-all-item"),
    # path('placeorder', views.placeorder, name="placeorder")
]
