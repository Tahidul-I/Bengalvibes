from django.db import models
from ..user.models import User
from ..products.models import ProductVariation
# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    address = models.TextField()
    postal_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=50)
    message = models.TextField(null=True)
    total_price = models.IntegerField()
    payment_mode = models.CharField(max_length=150)
    payment_id = models.CharField(max_length=250)
    delivery_fee = models.FloatField()
    order_statuses = (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered')
    )
    status = models.CharField(max_length=50, choices=order_statuses, default="Pending")
    tracking_no = models.CharField(max_length=150, null=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']
        def __str__(self):
            return self.tracking_no
        

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name="ordered_products")
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    quantity = models.PositiveIntegerField(null=False)

    def __str__(self):
        return '{}'.format(self.order.tracking_no)
    
    @property
    def total_price(self):
        return self.price * self.quantity

