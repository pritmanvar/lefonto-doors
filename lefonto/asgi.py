"""
ASGI config for tart project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lefonto.settings')
import django
django.setup()
from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from django.contrib.staticfiles import finders
import pathlib
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from authentication.routes import auth_router
from contactus.routes import contactus_router
from product.routes import product_router
from catalog.routes import catalog_router
from home.routes import home_router

from django.core.asgi import get_asgi_application

apps.populate(settings.INSTALLED_APPS)
def get_application() -> FastAPI:
    app = FastAPI(title="tart", debug=settings.DEBUG)
    SECRET_KEY = "wqwq"
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    static_path = os.path.join(settings.BASE_DIR, "staticfile")  # adjust if needed
    app.mount("/staticfile", StaticFiles(directory=static_path), name="static")

    app.include_router(auth_router, tags=["Auth"], prefix='/api/auth')
    app.include_router(contactus_router, tags=["Contactus"], prefix='/api/contactus')
    app.include_router(product_router, tags=["Product"], prefix='/api/product')
    app.include_router(catalog_router, tags=["Catalog"], prefix='/api/catalog')
    app.include_router(home_router, tags=["Home"], prefix='/api/home')
    app.mount("/", WSGIMiddleware(get_wsgi_application()))

    return app

app = get_application()