from django.db import models
from authentication.models import Location
from django.utils.safestring import mark_safe
# Create your models here.
class WhyUsCatalog(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='why_us_catalog/', null=True, blank=True)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.title if self.title else "Why Us Section"
    
    
class Catalog(models.Model):
    about = models.TextField(blank=True)
    why_us = models.ManyToManyField(WhyUsCatalog, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='catalog/', null=True, blank=True)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'
    
    def __str__(self):
        return "Catalog Page"

