from django.urls import path
from . import views

urlpatterns = [
    path('payment_gateway<str:track_no>',views.payment_gateway,name="payment_gateway"),
    path('payment_complete',views.payment_complete,name="payment_complete"),
    path('order_page<str:payment_status>',views.order_page,name="order_page"),
]
