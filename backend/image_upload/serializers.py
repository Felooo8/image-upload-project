from rest_framework import serializers
from .models import Tier, Image, ThumbnailImage
from django.contrib.auth.models import User


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)
        

class ThumbnailImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbnailImage
        fields = ('thumbnail', 'thumbnail_size',)
