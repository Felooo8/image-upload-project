from django.urls import path
from .views import ListImageView, ImageUploadView, ImageExpiringLinkView, CreateExpiringLink

urlpatterns = [
    path('images/', ListImageView.as_view(), name='image-list'),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('images/<image_id>/expiring-link/', CreateExpiringLink.as_view(), name='expiring-link'),
    path('<str:signed_url>/<str:signed_exp>', ImageExpiringLinkView.as_view(), name='expiring_image'),
]
