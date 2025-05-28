from django.db import models
from product.models import Product
from authentication.models import User

# Create your models here.
class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.PositiveIntegerField()
    message = models.TextField()
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    landmark = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Query from {self.name} - {self.mobile}" if self.name else "Contact Query"