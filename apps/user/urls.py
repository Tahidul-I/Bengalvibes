from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('user_login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='logout'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user-orders', views.user_orders, name='user-orders'),
    path('user-order-details/<int:id>', views.user_order_details, name='user-order-details')
]
