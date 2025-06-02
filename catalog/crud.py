import django
from utils.utils import CommonResponse

from catalog.models import Catalog
from fastapi import status

# ****************************************************** Get Catalog Details ******************************************************

def get_catalog_details(response):
    try:
        catalog = Catalog.objects.latest('id')

        catelog_object = {
            'id': catalog.id,
            'image': catalog.image.url if catalog.image else None,
            'about': catalog.about,
            'why_us': [
                {
                    'id': why_us.id,
                    'title': why_us.title,
                    'description': why_us.description,
                    'image': why_us.image.url if why_us.image else None
                }
                for why_us in catalog.why_us.all()
            ],
            'description': catalog.description,
            'location': {
                'id': catalog.location.id,
                'country': catalog.location.country,
                'state': catalog.location.state,
                'city': catalog.location.city,
                'pincode': catalog.location.pincode,
                'landmark': catalog.location.landmark,
            } if catalog.location else None
        }
        return CommonResponse(200, "True", 200, "Catalog fetched successfully.", 'success', Value=catelog_object)
    except Catalog.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return CommonResponse(404, "False", 404, "No catalog found.", 'error', Value=None)
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "False", 500, str(e), 'error', Value=None)