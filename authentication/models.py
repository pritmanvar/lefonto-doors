from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import uuid
from django.utils.safestring import mark_safe


class Location(models.Model):
    country = models.CharField(max_length=50, null=True, blank=True, default='India')
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    landmark = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country + " " + self.state + " " + self.city + " " + self.pincode + " " + self.landmark

class User(AbstractUser):
    USER_ROLES = (('admin', 'Admin'), ('dealer', 'dealer'),)
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    username = None
    name = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.PositiveBigIntegerField(unique=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='dealer')
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_image = models.FileField(upload_to='profile_images/', null=True, blank=True)
    
    def image_tag(self):
        if self.profile_image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.profile_image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Profile Image'
    
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.mobile) + " " + self.name if self.name else str(self.mobile)