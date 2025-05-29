import re
from authentication.models import User


class validate:

    def __init__(self, string):
        self.string = str(string)

    def Email(self):
        ptn = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        return re.match(ptn, str(self.string))

    def PhoneNumber(self):
        ptn = "^[6-9]\d{9}$"
        return re.match(ptn, str(self.string))

    def password(self):
        ptn = re.compile(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
        # print(self.string)
        return re.match(ptn, self.string)

    def date(self):
        ptn = re.compile(
            "/^\d{4}(\-)(((0)[0-9])|((1)[0-2]))(\-)([0-2][0-9]|(3)[0-1])$/gm")
        return re.match(ptn, self.string)

    def length(self, min_length: int, max_length: int):
        length = len(self.string)
        if length >= min_length and length <= max_length:
            return True
        return False

    def trueOrFalse(self):
        ptn = r"^true$|^false$"
        return re.match(ptn, str(self.string).lower())

    def emailOrPhoneNumberOrBoth(self):
        ptn = "^email$|^phoneNumber$|^both$"
        return re.match(ptn, self.string)

    def emailOrPhoneNumber(self):
        ptn = "^email$|^phoneNumber$"
        return re.match(ptn, self.string)

    def isInteger(self):
        try:
            float(self.string)
            return True
        except:
            return False


def resetPasswordDataValidation(data):
    Error = dict()
    if not validate(data.email).Email():
        Error["email Value Error"] = "Incorrect Email Format."
        return Error

    if not validate(data.newPassword).password():
        Error["newPassword Value Error"] = "Must Be Contains Uppercase, Lowercase Letters, Numbers, Special Characters And Length Is Greater Than 8 Character And Less Then 16 Character."
        return Error

    return None


def changePasswordDataValidation(data):
    Error = dict()
    try:
        # if not validate(data.email).Email():
        #     Error["email Value Error"] = "Incorrect Email Format."
        #     return Error

        if not validate(data.oldPassword).password():
            Error["oldPassword Value Error"] = "Must Be Contains Uppercase, Lowercase Letters, Numbers, Special Characters And Length Is Greater Than 8 Character And Less Then 16 Character."
            return Error

        if not validate(data.newPassword).password():
            Error["newPassword Value Error"] = "Must Be Contains Uppercase, Lowercase Letters, Numbers, Special Characters And Length Is Greater Than 8 Character And Less Then 16 Character."
            return Error
    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def loginDataValidation(data):
    Error = dict()
    if not validate(data.email).Email():
        Error = "Incorrect Email Format."
        return Error

    if not validate(data.password).password():
        Error["Password Value Error"] = "Must Be Contains Uppercase, Lowercase Letters, Numbers, Special Characters And Length Is Greater Than 8 Character And Less Then 16 Character."
        return Error

    return None


def paymentDataValidation(data):
    Error = dict()
    try:
        if not validate(data.email).Email():
            Error["email Value Error"] = "Incorrect Email Format."
            return Error

    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def emailVerifyDataValidation(data):
    Error = dict()
    try:

        if not validate(data.email).Email():
            Error["email Value Error"] = "Incorrect Email Format."
            return Error

    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def sendOTPDataValidation(data):
    Error = dict()

    if not validate(data.medium).emailOrPhoneNumber():
        Error["Medium Value Error"] = "Either An 'email' Or 'phoneNumber' Are Expected Strings."
        return Error

    if data.medium == 'phoneNumber':
        if not validate(data.phoneNumber).PhoneNumber():
            Error["phoneNumber Value Error"] = "Incorrect Phone Number Format."
            return Error

    if data.medium == 'email':
        if not validate(data.email).Email():
            Error["Email Value Error"] = "Incorrect Email Format."
            return Error

    if not (data.phoneNumber or data.email):
        Error["Email, PhoneNumber Value Error"] = "Email and Phonenumber can not be empty."
        return Error

    return None


def sendEmailOTPDataValidation(email):
    Error = dict()

    if not validate(email).Email():
        Error["Email Value Error"] = "Incorrect Email Format."
        return Error

    return None


def verifyOTPDataValidation(data):
    Error = dict()
    try:

        if not validate(data.phoneNumber).PhoneNumber():
            Error["phoneNumber Value Error"] = "Incorrect Phone Number Format."
            return Error
    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error
    return None


def UserCreateDataValidation(data):
    Error = dict()
    try:
        if not validate(data.email).Email():
            Error = "Incorrect Email Format."
            return Error
        else:
            try:
                user = User.objects.get(
                    email=data.email)
                Error = "Email Is already In Use."
                return Error
            except:
                pass

        if data.user_type not in ('customer', 'seller', 'seller_customer', 'freelancer'):
            Error = "user_type can be normal or seller or freelancer only"
            return Error

        if not validate(data.password).password():
            Error = "Password Must Be Contains Uppercase, Lowercase Letters, Numbers, Special Characters And Length Is Greater Than 8 Character And Less Then 16 Character."
            return Error

    except AttributeError as e:
        Error = str(e)
        return Error

    except Exception as e:
        Error = str(e)
        return Error

    return None

def sendSMSOTPDataValidation(data):
    Error = dict()

    if not validate(data.phone_number).PhoneNumber():
        Error["phone number Value Error"] = "Incorrect Phone Number Format."
        return Error

    return None


def verifyOTPDataValidation(data):
    Error = dict()
    try:
        if not validate(data.phone_number).PhoneNumber():
            Error["phone number Value Error"] = "Incorrect Phone Number Format."
            return Error
    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error
    return None



def UserUpdateDataValidation(email, data):
    Error = dict()
    try:
        if not validate(data.name).length(0, 50):
            Error["name Value Error"] = "Length Must Be Less Then 50."
            return Error

        if not validate(data.email).Email():
            Error = "Incorrect Email Format."
            return Error
        else:
            try:
                user = User.objects.get(
                    email=data.email)

                if (user.email != email):
                    Error = "Email Is already In Use."
                    return Error
            except:
                pass

        if not validate(data.mobile).PhoneNumber():
            Error["phoneNumber Value Error"] = "Incorrect Phone Number Format."
            return Error

    except AttributeError as e:
        Error = str(e)
        return Error

    except Exception as e:
        Error = str(e)
        return Error

    return None


def addDeliveryAddressDataValidation(data):
    Error = dict()
    try:
        if not validate(data.name).length(0, 70):
            Error["name Value Error"] = "Length Must Be Less Then 70."
            return Error

        if not validate(data.email).Email():
            Error = "Incorrect Email Format."
            return Error

        if not validate(data.phone_number).PhoneNumber():
            Error["phoneNumber Value Error"] = "Incorrect phoneNumber Format."
            return Error

        if not validate(data.city).length(0, 70):
            Error["city Value Error"] = "Length Must Be Less Then 70."
            return Error

        if not validate(data.state).length(0, 70):
            Error["state Value Error"] = "Length Must Be Less Then 70."
            return Error

        if not validate(data.pin_code).isInteger():
            Error["pincode Value Error"] = "Pincode Must Be Integer"
            return Error

    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def createOrderDataValidation(data):
    Error = dict()
    try:
        if not validate(data.name).length(1, 70):
            Error["name Value Error"] = "Length Must Be Less Then 70."
            return Error

        if not validate(data.phone_number).PhoneNumber():
            Error["phoneNumber Value Error"] = "Incorrect phoneNumber Format."
            return Error

        if not validate(data.pin_code).isInteger():
            Error["pin_code Value Error"] = "pin_code Must Be Integer."
            return Error

        if not validate(data.state).length(0, 70):
            Error["state Value Error"] = "Length Must Be Less Then 70."
            return Error

        if not validate(data.city).length(0, 70):
            Error["city Value Error"] = "Length Must Be Less Then 70."
            return Error

        if not validate(data.total_amount).isInteger():
            Error["Total Amount Value Error"] = "Total Amount Must Be Integer"
            return Error
        if not validate(data.total_discount).isInteger():
            Error["Total Discount Value Error"] = "Total Amount Must Be Integer"
            return Error

    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def ContactDataValidation(data):
    Error = dict()
    try:
        if not validate(data.name).length(0, 50):
            Error["name Value Error"] = "Length Must Be Less Then 50."
            return Error

        if not validate(data.email).Email():
            Error = "Incorrect Email Format."
            return Error

        if not validate(data.phone_number).PhoneNumber():
            Error["phone_number Value Error"] = "Incorrect Phone Number Format."
            return Error

    except AttributeError as e:
        Error = str(e)
        return Error

    except Exception as e:
        Error = str(e)
        return Error

    return None


def ConsultancyDataValidation(data):
    Error = dict()
    try:
        if not validate(data.phone_number).PhoneNumber():
            Error["phone_number Value Error"] = "Incorrect Phone Number Format."
            return Error

    except AttributeError as e:
        Error = str(e)
        return Error

    except Exception as e:
        Error = str(e)
        return Error

    return None

def sellerCreateDataValidation(data):
    Error = dict()
    try:
        if not validate(data.email).Email():
            Error["email Value Error"] = "Incorrect Email Format."
            return Error

        # if not validate(data.phoneNumber).PhoneNumber():
        #     Error["phone_number Value Error"] = "Incorrect Phone Number Format."
        #     return Error

        if not validate(data.name).length(1, 50):
            Error["name Value Error"] = "Name must be between 1 and 50 characters."
            return Error

        if not validate(data.gender) not in ['Male', 'Male']:
            Error["gender Value Error"] = "Gender must be Male or Male."
            return Error

        if not validate(data.country).length(1, 100):
            Error["country Value Error"] = "Country must be between 1 and 100 characters."
            return Error
        if not validate(data.state).length(1, 100):
            Error["country Value Error"] = "Country must be between 1 and 100 characters."
            return Error

        if not validate(data.city).length(1, 100):
            Error["city Value Error"] = "City must be between 1 and 100 characters."
            return Error


        if data.sellingType.lower() not in ['art', 'drawings']:
            Error["selling_type Value Error"] = "Selling type must be 'art' or 'Drawings'."
            return Error

        # Add additional validation rules as needed for other fields

    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def sellerStoreDataValidation(data):
    Error = dict()
    try:
        print(data)

        if not validate(data.storeName).length(1, 100):
            Error["store_name Value Error"] = "Store name must be between 1 and 100 characters."
            return Error

        if data.address:
            if not validate(data.address).length(1, 500):
                Error["address Value Error"] = "Address must be between 1 and 500 characters."
                return Error

        # Add additional validation rules as needed for other fields

    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None


def sellerPanCardDataValidation(data):
    Error = dict()
    try:
        if len(data) != 10:
            Error["panCardNumber Length Error"] = "PAN card number must be exactly 10 characters long."
            return Error

        # Add additional validation rules as needed for other fields

    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None

def orderStatusDataValidation(data):
    Error = dict()
    try:
        if data.status not in ["Confirmed","Shipped","Delivered","Canceled","Returned"]:
            Error["status Error"] = "Invalid status"
            return Error

        # Add additional validation rules as needed for other fields

    except AttributeError as e:
        Error["AttributeError"] = str(e)
        return Error

    except Exception as e:
        Error["Error"] = str(e)
        return Error

    return None
