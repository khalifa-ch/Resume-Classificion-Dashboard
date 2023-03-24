
from django.urls import path, re_path
from apps.home import views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('resume_classification', views.Classification, name='Classification'),

    
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 