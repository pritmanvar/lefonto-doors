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


    app.mount("/", WSGIMiddleware(get_wsgi_application()))

    return app

app = get_application()