import django
from utils.utils import (
    create_access_token,
    create_refresh_token,
    verify_access_token,
    CommonResponse,
    TokenResponse,
    UserResponse
)
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FTC.settings')
django.setup()
from django.contrib.auth import authenticate
from django.db import InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from authentication.models import User
from fastapi import status
from django.core.files.uploadedfile import InMemoryUploadedFile

# ****************************************************** Handle Login ******************************************************

def verify_credentials(data):
    try:
        user = User.objects.get(email = data.email)
        userdata = authenticate(email=user.email, password=data.password)
        if userdata is not None:
            return TokenResponse(access_token=create_access_token(userdata.email), refresh_token=create_refresh_token(userdata.email), Response=200, Error="False", ErrorCode=0, ResponseMessage="Successfully Logged In.", Message="Successfully Logged In.",Value={"email": userdata.email, "name": userdata.name})
        return TokenResponse(access_token="", refresh_token="", Response=401, Error="True", ErrorCode=0, ResponseMessage="Incorrect email or Password.", Message="Incorrect email or Password.")

    except User.DoesNotExist:
        return TokenResponse(access_token="", refresh_token="", Response=500, Error="True", ErrorCode=0, ResponseMessage="User does not exist.", Message='User does not exist.')
        
    except (InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        return TokenResponse(access_token="", refresh_token="", Response=500, Error="True", ErrorCode=0, ResponseMessage="Something went wrong, Please try again.", Message=("{}").format(error))

# ****************************************************** Update Profile Image ******************************************************

def update_profile_img(email, data, response):
    try:
        print(data)
        my_user = User.objects.get(email=email)

        uploaded_file = InMemoryUploadedFile(
            data.file, None, data.filename, None, data.content_type, None
        )

        my_user.profile_image.save(data.filename, uploaded_file, save=True)

        user_response = {'profile_image': my_user.profile_image.url if my_user.profile_image else ''}
        response.status_code = status.HTTP_200_OK
        return UserResponse(user_response, Response=200, Error="False", ErrorCode=0, ResponseMessage="Profile Image Updated.", Message="Profile Image Updated.")

    except User.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return UserResponse({}, 404, "True", 404, "User not found", 'user_not_found')

    except (InterfaceError, Error, DatabaseError, Exception, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return UserResponse({}, 500, "True", 500, "Something went wrong, Please try again.", ("{}").format(error))

# ****************************************************** Update Profile ******************************************************

def update_profile(email, data, response):
    try:
        my_user = User.objects.get(email=email)

        my_user.name = data.name
        my_user.email = data.email
        my_user.mobile = data.mobile
        my_user.address_house_no = data.address_house_no
        my_user.address_landmark = data.address_landmark
        my_user.address_city = data.address_city
        my_user.address_pincode = data.address_pincode
        my_user.address_state = data.address_state
        my_user.address_country = data.address_country
        
        my_user.save()
        
        response.status_code = status.HTTP_200_OK
        return TokenResponse(access_token=create_access_token(my_user.email), refresh_token=create_refresh_token(my_user.email), Response=200, Error="False", ErrorCode=0, ResponseMessage="Profile Updated.", Message="Profile Updated.",Value={"email": my_user.email, "name": my_user.name})

    except User.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return UserResponse({}, 404, "True", 404, "User not found", 'user_not_found')

    except (InterfaceError, Error, DatabaseError, Exception, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return UserResponse({}, 500, "True", 500, "Something went wrong, Please try again.", ("{}").format(error))

# ****************************************************** Get Profile ******************************************************

def get_profile_details(email, response):
    try:
        my_user = User.objects.get(email=email)

        user_response = {"email": my_user.email,
                         "name": my_user.name,
                         "role": my_user.role,
                         "address_house_no": my_user.address_house_no,
                         "address_landmark": my_user.address_landmark,
                         "address_city": my_user.address_city,
                         "address_pincode": my_user.address_pincode,
                         "address_state": my_user.address_state,
                         "address_country": my_user.address_country,
                         "mobile": my_user.mobile,
                         "profile_image": my_user.profile_image.url if my_user.profile_image else '',
                         }
        
        response.status_code = status.HTTP_200_OK
        return UserResponse(user_response, 200, "True", 200, "User Profile Fetched", 'success')

    except User.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return UserResponse({}, 404, "True", 404, "User not found", 'user_not_found')

    except (InterfaceError, Error, DatabaseError, Exception, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return UserResponse({}, 500, "True", 500, "Something went wrong, Please try again.", ("{}").format(error))


