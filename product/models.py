from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to='uploads/categories/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class ProductMaterial(models.Model):
    material_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.material_name

class Style(models.Model):
    style_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.style_name

class Color(models.Model):
    color_name = models.CharField(max_length=30, unique=True)
    color_code = models.CharField(max_length=7, unique=True)  # e.g., '#FFFFFF'

    def __str__(self):
        return self.color_name

class Size(models.Model):
    height = models.FloatField()
    width = models.FloatField()

    def __str__(self):
        return f"{self.height}x{self.width}"

class Feature(models.Model):
    feature_name = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to='uploads/features/', null=True, blank=True)
    
    def __str__(self):
        return self.feature_name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    details = models.TextField()
    short_description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    material = models.ForeignKey(ProductMaterial, on_delete=models.SET_NULL, null=True, blank=True)
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, blank=True)
    thickness = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    color = models.ManyToManyField(Color, blank=True)
    features = models.ManyToManyField(Feature, blank=True)
    warranty_details = models.TextField(blank=True)
    return_policy = models.TextField(blank=True)
    ratings = models.FloatField(default=0.0)
    recommanded_products = models.ManyToManyField('self', blank=True, symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_image = models.ImageField(upload_to='uploads/main_images/', null=True, blank=True)

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.FloatField(default=0)

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.product_name} - {self.size}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/additional_product_images/')

    def __str__(self):
        return f"{self.product.product_name} - Image"