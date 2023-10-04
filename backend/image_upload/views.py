from image_upload.image_utils import generate_thumbnails, sign_image_url
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .models import Image, Account, ThumbnailImage
from .serializers import ImageSerializer, ThumbnailImageSerializer
from django.core.signing import BadSignature
from django.core import signing
from rest_framework.permissions import AllowAny


class ListImageView(APIView):
    def get(self, request, format=None):
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            return Response("Account not found for the current user.", status=status.HTTP_400_BAD_REQUEST)
        
        response_data = []
        images = Image.objects.filter(user=request.user)

        for image in images:
            data = {}
            if account.tier.link_to_original:
                serializer = ImageSerializer(image, context={'request': request})

                data['original'] = serializer.data

            thumbnails = ThumbnailImage.objects.filter(original_image=image)
            thumbnail_serializer = ThumbnailImageSerializer(thumbnails, many=True, context={'request': request})

            data['thumbnails'] = thumbnail_serializer.data

            response_data.append(data)
        return Response(response_data, status=status.HTTP_200_OK)


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):

        serializer = ImageSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        image = serializer.save(user=request.user)
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            return Response("Account not found for the current user.", status=status.HTTP_400_BAD_REQUEST)
        thumbnail_urls = generate_thumbnails(image, account.tier.thumbnail_sizes, request)

        response_data = {
            "thumbnails": thumbnail_urls,
        }

        if account.tier.link_to_original:
            response_data["original_image"] = serializer.data

        if account.tier.expiring_link:
            try:
                expiration_seconds = int(request.data.get('expiration', 3600))  # Default to 1 hour if not specified
            except (TypeError, ValueError):
                expiration_seconds = 3600
            expiration_seconds = max(300, min(expiration_seconds, 30000))  # Ensure within the range 300-30000
            expiring_link = sign_image_url(image.image.url, expiration_seconds, request)
            response_data["expiring_link"] = expiring_link

        return Response(response_data, status=status.HTTP_201_CREATED)


class ImageExpiringLinkView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, signed_url, signed_exp):
        if signed_url is None or signed_exp is None:
            data = {"Error": "Something went wrong"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            expiration_seconds = signing.loads(signed_exp)
            image_url = signing.loads(signed_url, max_age=expiration_seconds)
            url = request.build_absolute_uri(image_url)
            data = {f"Image Expiring Link ({expiration_seconds}s)": url}
            return Response(data, status=status.HTTP_200_OK)
        except BadSignature:
            data = {"Error": "Invalid signature"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CreateExpiringLink(APIView):
    def post(self, request, image_id, format=None):

        if not image_id.isdigit():
            return Response({"Error": "Invalid image id format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response({"Error": "Image not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            return Response({"Error": "Account not found for the current user."}, status=status.HTTP_400_BAD_REQUEST)

        if not account.tier.expiring_link:
            return Response({"Error": "You do not have permission to create an expiring link. Please upgrade your plan."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            expiration_seconds = int(request.data.get('expiration', 3600))  # Default to 1 hour if not specified
        except (TypeError, ValueError):
            expiration_seconds = 3600
        expiration_seconds = max(300, min(expiration_seconds, 30000))  # Ensure within the range 300-30000

        expiring_link = sign_image_url(image.image.url, expiration_seconds, request)
        
        response_data = {
            "expiring_link": expiring_link
        }

        return Response(response_data, status=status.HTTP_200_OK)
