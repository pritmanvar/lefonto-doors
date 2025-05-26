from django.db import models

# Create your models here.
class WhyUsAbout(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/why_us_about/', null=True, blank=True)

    def __str__(self):
        return self.title if self.title else "Why Us Section"
    
class Expertise(models.Model):
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title if self.title else "Expertise Section"

class About(models.Model):
    background_image = models.ImageField(upload_to='uploads/about/', null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    title_description = models.TextField(blank=True)
    why_us_description = models.TextField(blank=True)
    why_us_image = models.ImageField(upload_to='uploads/about_why_us_bg/', null=True, blank=True)
    why_us = models.ManyToManyField(WhyUsAbout, blank=True)
    image_2 = models.ImageField(upload_to='uploads/about/', null=True, blank=True)
    description = models.TextField(blank=True)
    question = models.CharField(max_length=255, blank=True)
    answer = models.TextField(blank=True)
    expertise = models.ManyToManyField(Expertise, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.title if self.title else "About Page"