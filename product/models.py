import os
from django.db import models
from authentication.models import User, Location
from django_jsonform.models.fields import JSONField, ArrayField
from django.utils.safestring import mark_safe


# Create your models here.
class DoorCategory(models.Model):
    title = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category_image = models.FileField(upload_to='categories/', null=True, blank=True)
    
    def image_tag(self):
        if self.category_image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.category_image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Category Image'

    def __str__(self):
        return self.title

class DoorStyle(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class DoorDimension(models.Model):
    THICKNESS_MEASURE = (('mm', 'mm'), ('cm', 'cm'))
    thickness_measure = models.CharField(max_length=10, choices=THICKNESS_MEASURE, default='mm')
    height_measure = models.CharField(max_length=10, choices=THICKNESS_MEASURE, default='mm')
    width_measure = models.CharField(max_length=10, choices=THICKNESS_MEASURE, default='mm')
    thickness = models.FloatField()
    height = models.FloatField()
    width = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.height}{self.height_measure}x{self.width}{self.width_measure}x{self.thickness}{self.thickness_measure}"

class DoorColor(models.Model):
    name = models.CharField(max_length=30, unique=True)
    color_code = models.CharField(max_length=7, unique=True)  # e.g., '#FFFFFF'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
class DoorMaterial(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Feature(models.Model):
    feature_name = models.CharField(max_length=30, unique=True)
    image = models.FileField(upload_to='features/', null=True, blank=True)
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.feature_name

def get_dimentions():
    dimentions = []

    try:
        dimentions_objs = DoorDimension.objects.all()
        for dim in dimentions_objs:
            dimentions.append(f"{dim.height}{dim.height_measure}x{dim.width}{dim.width_measure}x{dim.thickness}{dim.thickness_measure} - {dim.id}")
        print(dimentions)
        return dimentions
    except Exception as e:
        print(e)
        return []

def get_materials():
    materials = []
    try:
        materials_objs = DoorMaterial.objects.all()
        for material in materials_objs:
            materials.append(f"{material.name} - {material.id}")
        return materials
    except Exception as e:
        print(e)
        return []

def get_colors():
    colors = []
    try:
        colors_objs = DoorColor.objects.all()
        for color in colors_objs:
            colors.append(f"{color.name} -- {color.id} -- {color.color_code}")
        return colors
    except Exception as e:
        print(e)
        return []

class Image(models.Model):
    image = models.FileField(blank=True, upload_to='product/')

    def __str__(self):
        return (self.id)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

class Product(models.Model):
    def PRODUCT_VARIENTS_SCHEMA():
        SCHEMA = {
            'type': 'array',
            'items': {
                'type': 'dict',
                'keys': {
                    'dimensions': {
                        'type': 'string',
                        'choices': get_dimentions()
                    },
                    'material': {
                        'type': 'string',
                        'choices': get_materials()
                    },
                    'price': {
                        'type': 'number',
                        'default': 0
                    },
                    'discount': {
                        'type': 'number',
                        'default': 0,
                        'min': 0,
                        'max': 100
                    }
                }
            }
        }
        return SCHEMA
    
    def COLOR_SCHEMA():
        SCHEMA = {
            'type': 'array',
            'items': {
                'type': 'dict',
                'keys': {
                    'color': {
                        'type': 'string',
                        'choices': get_colors()
                    },
                    'images': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'format': 'file-url',
                            'handler': '/product/json-file-handler'
                        }
                    }
                }
            }
        }
        return SCHEMA
    
    product_name = models.CharField(max_length=100)
    details = models.TextField()
    short_description = models.TextField()
    ratings = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0, help_text="Weights is in the kg.")
    category = models.ForeignKey(DoorCategory, on_delete=models.SET_NULL, null=True, blank=True)
    variants = JSONField(schema=PRODUCT_VARIENTS_SCHEMA, null=True, blank=True)
    colors = JSONField(schema=COLOR_SCHEMA, null=True, blank=True)
    style = models.ForeignKey(DoorStyle, on_delete=models.SET_NULL, null=True, blank=True)
    features = models.ManyToManyField(Feature, blank=True)
    warranty_details = models.TextField(blank=True)
    return_policy = models.TextField(blank=True)
    location = models.ManyToManyField(Location, blank=True)
    recommanded_products = models.ManyToManyField('self', blank=True, symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    main_image = models.FileField(upload_to='main_images/', null=True, blank=True)

    def image_tag(self):
        if self.main_image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.main_image.url)
        else:
            return 'No Image Found'
    
    def get_image_url(self):
        return f"{os.getenv('BASE_URL')}{self.main_image.url}" if self.main_image else None

    def get_product_varients(self):
        return [{**varient, 'material': {'material_name': varient.get('material', '').split(' - ')[0],
                                              'material_id': varient.get('material', '').split(' - ')[1]},
                                  'dimensions': {'dimension_id': varient.get('dimensions', '').split(' - ')[1],
                                                 'height': varient.get('dimensions', '').split(' - ')[0].split('x')[0],
                                                 'width': varient.get('dimensions', '').split(' - ')[0].split('x')[1],
                                                 'thickness': varient.get('dimensions', '').split(' - ')[0].split('x')[2],
                                                 }
                } for varient in self.variants]
    image_tag.short_description = 'Main Image'

    def __str__(self):
        return self.product_name

class GallarySupporting(models.Model):
    image = models.FileField(upload_to='gallary_supportings/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallary_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallary_updated_by')

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    def __str__(self):
        return f"Gallary Supporting - {self.product} - {self.user}"