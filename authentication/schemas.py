from pydantic import BaseModel
from utils.schemas import responseParameter
from typing import Sequence

class UserCreate(BaseModel):
    email: str
    user_type: str = "normal"
    password: str
    storename: str = ""

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: str
    email: str
    phoneNumber: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class googleTokenVerify(BaseModel):
    access_token: str

    class Config:
        from_attributes = True
        
class resetPassword(BaseModel):
    email: str 
    newPassword: str 
    token: str 
    class Config:
        from_attributes = True

class changePassword(BaseModel):
    oldPassword: str 
    newPassword: str 

    class Config:
        from_attributes = True

class notificationUpdate(BaseModel):
    email_notification: bool
    chat_notification: bool
    
    class Config:
        from_attributes = True
        
class verifyOTP(BaseModel):
    phone_number: int
    phone_number_otp: int 
    class Config:
        from_attributes = True

class sendOTP(BaseModel):
    phone_number: int
    class Config:
        from_attributes = True
        
class verifyOtpResponse(BaseModel):
    token: str
    # refresh_token: str
    status: Sequence[responseParameter]
    
    class Config:
        from_attributes = True