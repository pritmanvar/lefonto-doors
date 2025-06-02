import django
from utils.utils import CommonResponse

from django.db import InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError
from contactus.models import Inquiry
from fastapi import status

# ****************************************************** Add Inquiry ******************************************************

def add_inquiry_details(response, data):
    try:
        inquiry = Inquiry.objects.create(name=data.name, mobile=data.mobile, message=data.message, country=data.country, state=data.state, city=data.city, pincode=data.pincode, landmark=data.landmark, address=data.address)
        return CommonResponse(200, "True", 200, "Inquiry Added Successfully.", 'success', Value={'inquiry_id': inquiry.id})
    
    except (InterfaceError, Error, Exception, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "True", 0, "Something went wrong, Please try again.", Message=("{}").format(error))
