from django.db import models

# Create your models here.
class WhyUsCatalog(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='why_us_catalog/', null=True, blank=True)

    def __str__(self):
        return self.title if self.title else "Why Us Section"
    
class Catalog(models.Model):
    image = models.ImageField(upload_to='catalog/', null=True, blank=True)
    about = models.TextField(blank=True)
    why_us = models.ManyToManyField(WhyUsCatalog, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return "Catalog Page"

