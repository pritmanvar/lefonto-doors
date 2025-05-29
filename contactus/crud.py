import django
from utils.utils import CommonResponse

from django.db import InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError
from contactus.models import Inquiry
from product.models import Product
from fastapi import status

# ****************************************************** Add Inquiry ******************************************************

def add_inquiry_details(response, data):
    try:
        product = Product.objects.get(id=data.product)
        inquiry = Inquiry.objects.create(name=data.name, mobile=data.mobile, message=data.message, country=data.country, state=data.state, city=data.city, pincode=data.pincode, landmark=data.landmark, address=data.address, product=product)
        return CommonResponse(200, "True", 200, "Inquiry Added Successfully.", 'success', Value={'inquiry_id': inquiry.id})
    
    except Product.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return CommonResponse(404, "True", 404, "Product Not Found.", 'error', Value=None)
    
    except (InterfaceError, Error, Exception, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "True", 0, "Something went wrong, Please try again.", Message=("{}").format(error))
