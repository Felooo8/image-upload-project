from django.urls import path
from .views import ListImageView, ImageUploadView

urlpatterns = [
    path('images/', ListImageView.as_view(), name='image-list'),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
]
