from django.db import models

# Create your models here.

from wearstore.models import User
from wearstore.models import Product
# Create your models here.
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return f"{self.product.productName} added to wishlist by  {self.user.username}"