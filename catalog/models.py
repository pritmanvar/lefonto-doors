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
        SCHEMA = {
            'type': 'array',
            'items': {
                'type': 'object',
                'keys': {
                    'order': {
                        'type': 'integer',
                        'default': 0,
                        'required': True
                    },
                    'about': {
                        'type': 'string',
                        'default': ''
                    },
                    'why_us': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'keys': {
                                'title': {
                                    'type': 'string',
                                    'default': ''
                                },
                                'description': {
                                    'type': 'string',
                                    'default': ''
                                },
                                'image': {
                                    'type': 'string',
                                    'format': 'file-url',
                                    'handler': '/catalog/json-file-handler'
                                }
                            }
                        }
                    },
                    'location': {
                        'type': 'string',
                        'choices': get_locations()
                    },
                    'description': {
                        'type': 'string',
                        'default': ''
                    },
                    'image': {
                        'type': 'string',
                        'format': 'file-url',
                        'handler': '/catalog/json-file-handler'
                    }
                }
            }
        }
        return SCHEMA
    catalog_details = JSONField(schema=CATALOG_SCHEMA, null=True, blank=True)
    
    def __str__(self):
        return f"Catalog Page - {self.id}"

