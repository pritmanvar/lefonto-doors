import django
from utils.utils import CommonResponse

from home.models import Home
from fastapi import status

# ****************************************************** Get Home Details ******************************************************

def get_home_details(response):
    try:
        home = Home.objects.latest('id')

        home_object = {
            'id': home.id,
            'title': home.title,
            'description': home.description,
            'background_image': home.background_image.url if home.background_image else None,
            'categories': [
                {
                    'id': category.id,
                    'title': category.title,
                    'image': category.category_image.url if category.category_image else None
                }
                for category in home.categories.all()
            ],
            'question': home.question,
            'answer': home.answer,
            'features': [
                {
                    'id': feature.id,
                    'title': feature.feature_name,
                    'image': feature.image.url if feature.image else None
                }
                for feature in home.features.all()
            ],
            'banner': [
                {
                    'id': banner.id,
                    'description': banner.description,
                    'image': banner.image.url if banner.image else None,
                    'product_material': banner.product_material.name if banner.product_material else None
                }
                for banner in home.banner.all()
            ]
        }
        return CommonResponse(200, "True", 200, "Home fetched successfully.", 'success', Value=home_object)
    except Home.DoesNotExist:
        return CommonResponse(404, "False", 404, "No home found.", 'error', Value=None)
    except Exception as e:
        return CommonResponse(500, "False", 500, str(e), 'error', Value=None)