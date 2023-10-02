from image_upload.image_utils import generate_thumbnails, sign_image_url
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .models import Image, Account
from .serializers import ImageSerializer
from django.core.signing import BadSignature
from django.core import signing


class ListImageView(APIView):
    def get(self, request, format=None):
        images = Image.objects.filter(user=request.user)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):

        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save(user=request.user)
            account = Account.objects.get(user=request.user)
            thumbnail_urls = generate_thumbnails(image, account)

            response_data = {
                "thumbnails": thumbnail_urls,
                "original_image": serializer.data if account.tier.link_to_original else None,
            }

            if account.tier.expiring_link:
                expiration_seconds = int(request.data.get('expiration', 3600))  # Default to 1 hour if not specified
                expiration_seconds = max(300, min(expiration_seconds, 30000))  # Ensure within the range 300-30000
                expiring_link = sign_image_url(image.image.url, expiration_seconds)
                response_data["expiring_link"] = expiring_link

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageExpiringLinkView(APIView):
    def get(self, request, signed_url, signed_exp):
        if signed_url is not None:
            try:
                expiration_seconds = signing.loads(signed_exp)
                image_url = signing.loads(signed_url, max_age=expiration_seconds)
                data = {"url": image_url}
                return Response(data, status=status.HTTP_200_OK)
            except BadSignature:
                data = {"Error": "Invalid signature"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        data = {"Error": "Something went wrong"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
