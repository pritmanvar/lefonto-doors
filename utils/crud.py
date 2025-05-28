import django
from django.db import InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError
import random

from django.core.cache import cache

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FTC.settings')
django.setup()

from authentication.models import User
from utils.utils import create_access_token, create_refresh_token, CommonResponse, TokenResponse
from utils.notification import twoFactor, Email


# ****************************************************** send otp using sms ******************************************************


def sendSmsOtp(data):
    sms = twoFactor()
    return sms.send(data.phoneNumber)

# ****************************************************** send otp using email ******************************************************


def sendEmailOtp(email):
    OTP = random.randint(1000, 9999)
    emailotp = Email()
    cache.set(email, OTP)
    return emailotp.send("OTP Verification", "Here is your OTP : " +
                         str(OTP), [email])

# ****************************************************** send otp ******************************************************


def sendOtp(data):
    try:
        if(data.medium == "email"):
            return sendEmailOtp(data.email)
        else:
            return sendSmsOtp(data)
    except Exception as e:
        return CommonResponse(200, "True", 0, "", Message=str(e))

# ****************************************************** verify email otp ******************************************************


def verifyEmailOtp(data):
    print(data)
    if cache.get(data.email) == data.emailOTP:
        return True
    return False
# ****************************************************** verify sms otp ******************************************************


def verifySmsOtp(data):
    sms = twoFactor()
    isSmsOtpVerified = sms.verify(data.phoneNumber, data.phoneNumberOTP)
    return isSmsOtpVerified

# ****************************************************** verify otp ******************************************************


def verifyOtp(data):
    if verifySmsOtp(data):
        return TokenResponse(access_token=create_access_token(data.phoneNumber), refresh_token=create_refresh_token(data.phoneNumber), Response=200, Error="False", ErrorCode=0, ResponseMessage="", Message="OTP Matched")
    return TokenResponse(access_token="", refresh_token="", Response=200, Error="False", ErrorCode=0, ResponseMessage="", Message="OTP is incorrect!")


# ****************************************************** Email available or not******************************************************


def isEmailAvailable(data):
    try:
        print(User.objects.all())
        user = User.objects.get(email=data.email)
        print(user)
        return CommonResponse(200, "False", 0, "", Message=("Email Is Already In Use."))

    except (InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        return CommonResponse(400, "True", 0, "", Message=("{}").format(error))

    except Exception as e:
        return CommonResponse(200, "False", 0, "", Message=("Email Is Available."))