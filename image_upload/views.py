from image_upload.image_utils import generate_thumbnails
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Image, Account
from .serializers import ImageSerializer

class ListImageView(APIView):
    def get(self, request, format=None):
        images = Image.objects.filter(user=request.user)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageUploadView(APIView):
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save(user=request.user)
            account = Account.objects.get(user=request.user)
            generate_thumbnails(image, account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
