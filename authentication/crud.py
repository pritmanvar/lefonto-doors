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
from authentication.models import User, Location
from fastapi import status
from django.core.files.uploadedfile import InMemoryUploadedFile

# ****************************************************** Handle Login ******************************************************

def verify_credentials(data):
    try:
        user = User.objects.get(mobile = data.mobile)
        userdata = authenticate(mobile=user.mobile, password=data.password)
        if userdata is not None:
            return TokenResponse(access_token=create_access_token(userdata.mobile), refresh_token=create_refresh_token(userdata.mobile), Response=200, Error="False", ErrorCode=0, ResponseMessage="Successfully Logged In.", Message="Successfully Logged In.",Value={"mobile": userdata.mobile, "name": userdata.name})
        return TokenResponse(access_token="", refresh_token="", Response=401, Error="True", ErrorCode=0, ResponseMessage="Incorrect mobile or Password.", Message="Incorrect mobile or Password.")

    except User.DoesNotExist:
        return TokenResponse(access_token="", refresh_token="", Response=500, Error="True", ErrorCode=0, ResponseMessage="User does not exist.", Message='User does not exist.')
        
    except (InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        return TokenResponse(access_token="", refresh_token="", Response=500, Error="True", ErrorCode=0, ResponseMessage="Something went wrong, Please try again.", Message=("{}").format(error))

# ****************************************************** Update Profile Image ******************************************************

def update_profile_img(mobile, data, response):
    try:
        print(data)
        my_user = User.objects.get(mobile=mobile)

        uploaded_file = InMemoryUploadedFile(
            data.file, None, data.filename, None, data.content_type, None
        )

        my_user.profile_image.save(data.filename, uploaded_file, save=True)

        user_response = {'profile_image': f"{os.getenv('BASE_URL')}{my_user.profile_image.url}" if my_user.profile_image else ''}
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

def update_profile(mobile, data, response):
    try:
        my_user = User.objects.get(mobile=mobile)

        my_user.name = data.name
        my_user.email = data.email
        my_user.mobile = data.mobile
        
        my_user.save()
        
        response.status_code = status.HTTP_200_OK
        return TokenResponse(access_token=create_access_token(my_user.mobile), refresh_token=create_refresh_token(my_user.mobile), Response=200, Error="False", ErrorCode=0, ResponseMessage="Profile Updated.", Message="Profile Updated.",Value={"mobile": my_user.mobile, "name": my_user.name})

    except User.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return UserResponse({}, 404, "True", 404, "User not found", 'user_not_found')

    except (InterfaceError, Error, DatabaseError, Exception, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return UserResponse({}, 500, "True", 500, "Something went wrong, Please try again.", ("{}").format(error))

# ****************************************************** Get Profile ******************************************************

def get_profile_details(mobile, response):
    try:
        my_user = User.objects.get(mobile=mobile)

        user_response = {"mobile": my_user.mobile,
                         "name": my_user.name,
                         "role": my_user.role,
                         "landmark": my_user.location.landmark if my_user.location else '',
                         "city": my_user.location.city if my_user.location else '',
                         "pincode": my_user.location.pincode if my_user.location else '',
                         "state": my_user.location.state if my_user.location else '',
                         "country": my_user.location.country if my_user.location else '',
                         "mobile": my_user.mobile,
                         "profile_image": f"{os.getenv('BASE_URL')}{my_user.profile_image.url}" if my_user.profile_image else '',
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

# ****************************************************** Get Location ******************************************************

def get_location_details(response):
    try:
        locations = list(Location.objects.all().values('country', 'state', 'city', 'pincode', 'landmark'))
        return CommonResponse(200, "True", 200, "Locations Fetched Successfully.", 'success', Value=locations)

    except (InterfaceError, Error, Exception, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "True", 0, "Something went wrong, Please try again.", Message=("{}").format(error))

# ****************************************************** Add Location ******************************************************

def add_location_details(response, data, mobile):
    try:
        user = User.objects.get(mobile=mobile)
        location, created = Location.objects.get_or_create(country=data.country, state=data.state, city=data.city, pincode=data.pincode, landmark=data.landmark)

        user.location = location
        user.save()

        if created:
            return CommonResponse(200, "True", 200, "Location Added Successfully.", 'success', Value={'location_id': location.id})
        return CommonResponse(200, "True", 200, "Location Already Exists.", 'success', Value={'location_id': location.id})
    
    except User.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return CommonResponse(404, "True", 404, "User not found.", 'error', Value=None)
    
    except (InterfaceError, Error, Exception, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "True", 0, "Something went wrong, Please try again.", Message=("{}").format(error))