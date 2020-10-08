from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.upload_file, name='uploadSeq-upload'),
    path('preview', views.preview_file, name='uploadSeq-preview')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
