from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-homepage'),
    path('help', views.help_view, name='main-help'),
    path('about', views.about_view, name='main-about'),
    path('index', views.IndexView.as_view(), name='index'),
    path('api-data/<slug:slug_analysis_code>', views.get_data, name='api-data'),
]
