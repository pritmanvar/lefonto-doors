from django.db import models
from authentication.models import Location
from django.utils.safestring import mark_safe
from django_jsonform.models.fields import JSONField

class Image(models.Model):
    image = models.FileField(blank=True, upload_to='catalog/')

    def __str__(self):
        return (self.id)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 70px; height:70px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

def get_locations():
    locations = []
    try:
        location_objs = Location.objects.all()
        for location in location_objs:
            locations.append(f"{location.country}, {location.state}, {location.city}, {location.pincode}, {location.landmark} - {location.id}")
        return locations
    except Exception as e:
        print(f"Error fetching locations: {e}")
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
                        "title": "About",
                        "type": "object",
                        "properties": {
                            "type": { "const": "about" },
                            "about": { "type": "string", "default": "" }
                        },
                        "required": ["type"]
                    },
                    {
                        "title": "Why Us",
                        "type": "object",
                        "properties": {
                            "type": { "const": "why_us" },
                            "why_us": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": { "type": "string" },
                                        "description": { "type": "string" },
                                        "image": {
                                            "type": "string",
                                            "format": "file-url",
                                            "handler": "/catalog/json-file-handler"
                                        }
                                    }
                                }
                            }
                        },
                        "required": ["type"]
                    },
                    {
                        "title": "Products List",
                        "type": "object",
                        "properties": {
                            "type": { "const": "products_list" },
                            "products_list": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": { "type": "string" },
                                        "description": { "type": "string" },
                                        "image": {
                                            "type": "string",
                                            "format": "file-url",
                                            "handler": "/catalog/json-file-handler"
                                        }
                                    }
                                }
                            }
                        },
                        "required": ["type"]
                    },
                    {
                        "title": "Single Product Image",
                        "type": "object",
                        "properties": {
                            "type": { "const": "product" },
                            "product": {
                                "type": "string",
                                "format": "file-url",
                                "handler": "/catalog/json-file-handler"
                            }
                        },
                        "required": ["type"]
                    },
                    {
                        "title": "Location Section",
                        "type": "object",
                        "properties": {
                            "type": { "const": "location" },
                            "location": {
                                "type": "string",
                                "enum": get_locations()
                            }
                        },
                        "required": ["type"]
                    }
                ]
            }
        }
        return SCHEMA
    catalog_details = JSONField(schema=CATALOG_SCHEMA, null=True, blank=True)
    
    def __str__(self):
        return f"Catalog Page - {self.id}"

