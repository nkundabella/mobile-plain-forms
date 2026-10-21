from django.urls import path
from . import views

app_name = 'showcase'

urlpatterns = [
    path('', views.form_showcase_view, name='form_showcase'),
    path('gallery/', views.image_gallery_view, name='image_gallery'),
]
