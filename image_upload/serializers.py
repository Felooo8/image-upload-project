from rest_framework import serializers
from .models import Tier, Image
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
        fields = ('id', 'image')
