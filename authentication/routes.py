from fastapi import APIRouter, Depends, File, UploadFile, Response

from utils.utils import get_token, TokenResponse
from utils.schemas import tokenResponse, userResponse, commonResponse
from utils.validation import loginDataValidation, UserUpdateDataValidation

from authentication.schemas import UserLogin, UserUpdate, Location
from authentication.crud import verify_credentials, update_profile, update_profile_img, get_profile_details, get_location_details, add_location_details

auth_router = APIRouter()

@auth_router.post("/login", summary="login here", response_model=tokenResponse)
def login(data: UserLogin):
    is_data_valid = loginDataValidation(data)
    if is_data_valid is not None:
        return TokenResponse(access_token="", refresh_token="", Response=406 , Error="True", ErrorCode=0, ResponseMessage="Unacceptable Parameter Value", Message=is_data_valid)
    return verify_credentials(data)

@auth_router.post("/update-profile-img", summary="update user profile img", response_model=userResponse)
def change_profile_image(response: Response, profile_img: UploadFile = File(...),  login_details=Depends(get_token)):
    print(profile_img)
    mobile = login_details['mobile']
    return update_profile_img(mobile, data=profile_img, response=response)

@auth_router.put("/profile", summary="update user details", response_model=tokenResponse)
def profile_update(response: Response, data: UserUpdate, login_details=Depends(get_token)):
    mobile = login_details['mobile']
    is_data_valid = UserUpdateDataValidation(mobile, data)
    if is_data_valid is not None:
        return TokenResponse(access_token="", refresh_token="", Response=500, Error="True", ErrorCode=0, ResponseMessage="Unacceptable Parameter Value.", Message=is_data_valid)
    
    return update_profile(mobile, data, response=response)

@auth_router.get('/profile', summary="get user details", response_model=userResponse)
def get_profile(response: Response, login_details=Depends(get_token)):
    print(login_details)
    mobile = login_details['mobile']
    print("MY mobile", mobile)
    return get_profile_details(mobile, response=response)

@auth_router.get('/location', summary="get location details", response_model=commonResponse)
def get_location(response: Response):
    return get_location_details(response=response)

@auth_router.post('/location', summary="add location", response_model=commonResponse)
def add_location(response: Response, data: Location, login_details=Depends(get_token)):
    mobile = login_details['mobile']
    return add_location_details(response=response, data=data, mobile=mobile)