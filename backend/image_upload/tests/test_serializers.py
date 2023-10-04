from django.test import TestCase
from image_upload.serializers import TierSerializer, UserSerializer, ImageSerializer, ThumbnailImageSerializer
from image_upload.models import Tier, Image, ThumbnailImage
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from image_upload.tests.tests_utils import create_image

class SerializersTestCase(TestCase):
    def test_serializers(self):
        tier_name = 'Basic'
        tier_sizes = '200,400,500'
        tier = Tier.objects.create(name=tier_name, thumbnail_sizes=tier_sizes, link_to_original=True)

        username = 'testuser'
        user = User.objects.create_user(username=username, password='testpassword')

        image_title = 'image_file.png'
        thumbnail_size = 200
        fake_image = create_image(None, 'image.png')
        image_file = SimpleUploadedFile(image_title, fake_image.getvalue())
        image = Image.objects.create(user=user, image=image_file)
        thumbnail_image = ThumbnailImage.objects.create(original_image=image, thumbnail_size=thumbnail_size, thumbnail=image_file)

        tier_serializer = TierSerializer(instance=tier)
        user_serializer = UserSerializer(instance=user)
        image_serializer = ImageSerializer(instance=image)
        thumbnail_image_serializer = ThumbnailImageSerializer(instance=thumbnail_image)

        self.assertEqual(tier_serializer.data['name'], tier_name)
        self.assertEqual(tier_serializer.data['thumbnail_sizes'], tier_sizes)
        self.assertEqual(tier_serializer.data['link_to_original'], True)
        self.assertEqual(user_serializer.data['username'], username)
        self.assertEqual(image_serializer.data['image'], image.image.url)
        self.assertEqual(thumbnail_image_serializer.data['thumbnail_size'], thumbnail_size)
