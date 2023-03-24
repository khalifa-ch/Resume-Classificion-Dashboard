
from django.contrib import admin
from django.urls import path, include  
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), #  login / register
    path("", include("apps.home.urls"))             
]

