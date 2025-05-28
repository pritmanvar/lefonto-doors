from django.db import models
from product.models import DoorMaterial, DoorCategory, Feature

# Create your models here.
class Banner(models.Model):
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='uploads/banners/', null=True, blank=True)
    product_material = models.ForeignKey(DoorMaterial, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Home(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    background_image = models.ImageField(upload_to='uploads/home/', null=True, blank=True)
    categories = models.ManyToManyField(DoorCategory, blank=True)
    question = models.CharField(max_length=255, blank=True)
    answer = models.TextField(blank=True)
    features = models.ManyToManyField(Feature, blank=True)

    def __str__(self):
        return self.title if self.title else "Home Page"