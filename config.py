import os
from dotenv import load_dotenv
import urllib

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    POSTGRES_USER : str =  os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD : str = str(os.getenv("POSTGRES_PASSWORD"))
    POSTGRES_SERVER : str = str(os.getenv("POSTGRES_SERVER","localhost"))
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5432) # default postgres port is 5432
    POSTGRES_DB : str = str(os.getenv("POSTGRES_DB","tdd"))
    JWT_SECRET_KEY : str = str(os.getenv("JWT_SECRET_KEY","key"))
    JWT_REFRESH_SECRET_KEY : str = str(os.getenv("JWT_REFRESH_SECRET_KEY","secret key"))
    ACCESS_TOKEN_EXPIRE_MINUTES : int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",1440)) # 60 * 24 = 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES : int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES",11340))# 60 * 24 * 7 = 7day
    ALGORITHM : str = str(os.getenv("ALGORITHM","HS256"))
    EMAIL_HOST_USER : str = str(os.getenv("EMAIL_HOST_USER"))
    EMAIL_HOST_PASSWORD : str = str(os.getenv("EMAIL_HOST_PASSWORD"))
    SMSAPI : str = str(os.getenv("SMSAPI"))
    RAZORPAY_ID : str =  os.getenv("RAZORPAY_ID")
    RAZORPAY_KEY : str = str(os.getenv("RAZORPAY_KEY"))
    TWILIO_ACCOUNT_SID : str =  str(os.getenv("TWILIO_ACCOUNT_SID"))
    TWILIO_AUTH_TOKEN : str = str(os.getenv("TWILIO_AUTH_TOKEN"))
    GOOGLE_CLIENT_ID : str = str(os.getenv("GOOGLE_CLIENT_ID"))
    TAX_PERCENTAGE = 18
settings = Settings()