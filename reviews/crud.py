import django
from utils.utils import CommonResponse

from reviews.models import CustomerReview
from fastapi import status
from authentication.models import User
from product.models import Product

# ****************************************************** Add Review ******************************************************

def add_review_details(response, data, user_email):
    try:
        user = User.objects.get(email=user_email)
        product = Product.objects.get(id=data.product)
        review = CustomerReview.objects.create(user=user, product=product, rating=data.rating, review_text=data.review_text)
        return CommonResponse(200, "True", 200, "Review added successfully.", 'success', Value={'review_id': review.id})
    except User.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return CommonResponse(404, "False", 404, "User not found.", 'error', Value=None)
    except Product.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return CommonResponse(404, "False", 404, "Product not found.", 'error', Value=None)
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "False", 500, str(e), 'error', Value=None)