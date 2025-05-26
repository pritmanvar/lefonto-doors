from django.db import models

# Create your models here.
class ContactQueries(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query from {self.name} - {self.email}" if self.name else "Contact Query"