from django.urls import path
from catalog import views


urlpatterns = [
   path("json-file-handler",views.file_handler,name="file handler"),
]