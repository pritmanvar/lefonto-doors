from django.db import models
from authentication.models import Location
from django.utils.safestring import mark_safe
from django_jsonform.models.fields import JSONField
from product.models import Product
import os


class Image(models.Model):
    image = models.FileField(blank=True, upload_to="catalog/")

    def get_image_url(self):
        return f"{os.getenv('BASE_URL')}{self.image.url}" if self.image else None

    def __str__(self):
        return self.id

    def image_tag(self):
        if self.image:
            return mark_safe(
                '<img src="%s" style="width: 70px; height:70px;" />' % self.image.url
            )
        else:
            return "No Image Found"

    image_tag.short_description = "Image"


def get_locations():
    locations = []
    try:
        location_objs = Location.objects.all()
        for location in location_objs:
            locations.append(
                f"{location.country}, {location.state}, {location.city}, {location.pincode}, {location.landmark} - {location.id}"
            )
        return locations
    except Exception as e:
        print(f"Error fetching locations: {e}")
        return []


def get_products():
    products = []
    try:
        product_objs = Product.objects.all()
        for product in product_objs:
            products.append(f"{product.product_name} - {product.id}")
        return products
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []


class Catalog(models.Model):
    def CATALOG_SCHEMA():
        return {
            "type": "array",
            "title": "Catalog Sections",
            "items": {
                "title": "Section",
                "anyOf": [  # dynamically choose type
                    {
                        "title": "Banner",
                        "type": "object",
                        "properties": {
                            "banner_image": {
                                "type": "string",
                                "format": "file-url",
                                "handler": "/catalog/json-file-handler",
                            }
                        },
                    },
                    {
                        "title": "About Us",
                        "type": "object",
                        "properties": {
                            "about": {
                                "type": "array",
                                "items": {"type": "string"},
                                "default": [],
                            },
                        },
                    },
                    {
                        "title": "Why Choose Us",
                        "type": "object",
                        "properties": {
                            "why_us": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "description": {"type": "string"},
                                        "icon": {
                                            "type": "string",
                                            "format": "file-url",
                                            "handler": "/catalog/json-file-handler",
                                            "helpText": "Please upload SVG icons.",
                                        },
                                    },
                                },
                            },
                        },
                    },
                    {
                        "title": "Our Moto",
                        "type": "object",
                        "properties": {
                            "moto": {
                                "type": "object",
                                "properties": {
                                    "moto": {"type": "string", "default": ""},
                                    "logo": {
                                        "type": "string",
                                        "format": "file-url",
                                        "handler": "/catalog/json-file-handler",
                                        "helpText": "Please upload your logo.",
                                    },
                                },
                            }
                        },
                    },
                    {
                        "title": "Our Products",
                        "type": "object",
                        "properties": {
                            "products_list": {
                                "type": "array",
                                "title": "Products",
                                "items": {
                                    "type": "string",
                                    "choices": get_products(),
                                    "widget": "multiselect",
                                },
                            }
                        },
                    },
                    {
                        "title": "Feature Image",
                        "type": "object",
                        "properties": {
                            "feature_image": {
                                "type": "string",
                                "format": "file-url",
                                "handler": "/catalog/json-file-handler",
                            }
                        },
                    },
                    {
                        "title": "Size",
                        "type": "object",
                        "properties": {
                            "size": {
                                "type": "object",
                                "properties": {
                                    "length": {"type": "string"},
                                    "width": {"type": "string"},
                                    "thickness": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                },
                            }
                        },
                    },
                    {
                        "title": "Note",
                        "type": "object",
                        "properties": {
                            "notes": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                },
                            }
                        },
                    },
                ],
            },
        }

    catalog_details = JSONField(schema=CATALOG_SCHEMA, null=True, blank=True)

    def __str__(self):
        return f"Catalog Page - {self.id}"
