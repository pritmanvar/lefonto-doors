import django
from utils.utils import CommonResponse

from about.models import About
from fastapi import status

# ****************************************************** Get About Details ******************************************************

def get_about_details(response):
    try:
        about = About.objects.latest('id')
        about_object = {
            'id': about.id,
            'background_image': about.background_image.url if about.background_image else None,
            'title': about.title,
            'title_description': about.title_description,
            'why_us_description': about.why_us_description,
            'why_us_image': about.why_us_image.url if about.why_us_image else None,
            'why_us': [
                {
                    'id': why_us.id,
                    'title': why_us.title,
                    'description': why_us.description,
                    'image': why_us.image.url if why_us.image else None
                } 
                for why_us in about.why_us.all()
            ],
            'image_2': about.image_2.url if about.image_2 else None,
            'description': about.description,
            'question': about.question,
            'answer': about.answer,
            'expertise': [
                {
                    'id': expertise.id,
                    'title': expertise.title,
                }
                for expertise in about.expertise.all()
            ],
            'contact_number': about.contact_number,
            'email': about.email,
            'address': about.address,
            'website': about.website
        }
        return CommonResponse(200, "True", 200, "About fetched successfully.", 'success', Value=about_object)
    except About.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return CommonResponse(404, "False", 404, "No about found.", 'error', Value=None)
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "False", 500, str(e), 'error', Value=None)
    
    