from django.db import models
from ..products.models import ProductVariation
from ..user.models import User
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariation, on_delete=models.PROTECT, blank=True, null=True)
    product_quantity = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.product} - {self.user.username}"
    
    @property
    def total_price(self):
        return self.product.selling_price * self.product_quantity
    

