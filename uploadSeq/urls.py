from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='uploadSeq-upload'),
]
