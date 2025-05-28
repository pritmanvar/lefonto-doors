from django.urls import path,include
from product import views


urlpatterns = [
   path("json-file-handler",views.file_handler,name="file handler"),
]