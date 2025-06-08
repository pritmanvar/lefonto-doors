from django.db import models
from django.utils.safestring import mark_safe
from product.models import DoorMaterial, DoorCategory, Feature

# Create your models here.
class Banner(models.Model):
    description = models.CharField(max_length=255, blank=True)
    product_material = models.ForeignKey(DoorMaterial, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.FileField(upload_to='banners/', null=True, blank=True)
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

class Home(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(DoorCategory, blank=True)
    question = models.CharField(max_length=255, blank=True)
    answer = models.TextField(blank=True)
    features = models.ManyToManyField(Feature, blank=True)
    banner = models.ManyToManyField(Banner, blank=True)
    background_image = models.FileField(upload_to='home/', null=True, blank=True)

    def image_tag(self):
        if self.background_image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.background_image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Background Image'
    
    def __str__(self):
        return self.title if self.title else "Home Page"