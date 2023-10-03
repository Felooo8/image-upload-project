from django.test import TestCase
from image_upload.models import Tier, Account, Image, ThumbnailImage
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from image_upload.tests.tests_utils import create_image

class ModelsTestCase(TestCase):
    def test_models(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        tier = Tier.objects.create(name='Basic', thumbnail_sizes='200,400,500', link_to_original=True)
        account = Account.objects.create(user=user, tier=tier)

        image_title = 'image_file.png'
        thumbnail_size = 200
        fake_image = create_image(None, 'image.png')
        image_file = SimpleUploadedFile(image_title, fake_image.getvalue())
        image = Image.objects.create(user=user, image=image_file)
        thumbnail_image = ThumbnailImage.objects.create(original_image=image, thumbnail_size=thumbnail_size, thumbnail=image_file)

        self.assertEqual(str(tier), 'Basic')
        self.assertEqual(str(account), f'Account for {user.username}')
        self.assertEqual(str(image), f'Image {image.id}')
        self.assertEqual(str(thumbnail_image), f'Thumbnail for {thumbnail_image.original_image} - Size: {thumbnail_size}')
