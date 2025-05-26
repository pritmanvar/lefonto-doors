from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import uuid


class User(AbstractUser):
    id = models.CharField(max_length=36, primary_key=True,
                          default=uuid.uuid4())
    username = None
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=150, unique=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    sub_district = models.CharField(max_length=50, null=True, blank=True)
    street_name = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_google_login = models.BooleanField(default=False)
    # To create custom user
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
