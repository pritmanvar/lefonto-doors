from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
class WhyUsAbout(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='why_us_about/', null=True, blank=True)

    def __str__(self):
        return self.title if self.title else "Why Us Section"
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'
    
class Expertise(models.Model):
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title if self.title else "Expertise Section"

class About(models.Model):
    title = models.CharField(max_length=100, blank=True)
    title_description = models.TextField(blank=True)
    why_us_description = models.TextField(blank=True)
    why_us = models.ManyToManyField(WhyUsAbout, blank=True)
    description = models.TextField(blank=True)
    question = models.CharField(max_length=255, blank=True)
    answer = models.TextField(blank=True)
    expertise = models.ManyToManyField(Expertise, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    background_image = models.FileField(upload_to='about/', null=True, blank=True)
    why_us_image = models.FileField(upload_to='about_why_us_bg/', null=True, blank=True)
    image_2 = models.FileField(upload_to='about/', null=True, blank=True)

    def background_image_tag(self):
        if self.background_image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.background_image.url)
        else:
            return 'No Image Found'

    background_image_tag.short_description = 'Background Image'

    def why_about_us_image_tag(self):
        if self.why_us_image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.why_us_image.url)
        else:
            return 'No Image Found'

    why_about_us_image_tag.short_description = 'Wht about us Image'

    def image_2_tag(self):
        if self.image_2:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.image_2.url)
        else:
            return 'No Image Found'

    image_2_tag.short_description = 'Image 2'
    def __str__(self):
        return self.title if self.title else "About Page"