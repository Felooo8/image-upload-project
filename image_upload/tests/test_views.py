from django.urls import reverse
from image_upload.tests.tests_utils import create_image
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from image_upload.models import Account, Image, ThumbnailImage, Tier
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import signing
from rest_framework.test import APIClient

class ImageViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_2 = User.objects.create_user(username='testuser_2', password='testpassword')
        self.tier = Tier.objects.create(name='Plan 1', thumbnail_sizes='200,400,500', link_to_original=True)
        self.tier_2 = Tier.objects.create(name='Plan 2', thumbnail_sizes='200,500', expiring_link=True)
        self.account = Account.objects.create(user=self.user, tier=self.tier)
        self.account_2 = Account.objects.create(user=self.user_2, tier=self.tier_2)
        self.user_no_account = User.objects.create_user(username='testuser_no_account', password='testpassword')

        image = create_image(None, 'image.png')
        image_file = SimpleUploadedFile('image_file.png', image.getvalue())
        self.image = Image.objects.create(user=self.user, image=image_file)
        self.image_2 = Image.objects.create(user=self.user_2, image=image_file)

        self.thumbnail_image = ThumbnailImage.objects.create(original_image=self.image, thumbnail_size=200, thumbnail=image_file)
        self.thumbnail_image_2 = ThumbnailImage.objects.create(original_image=self.image, thumbnail_size=400, thumbnail=image_file)
        
        self.client = APIClient()
        self.client_2 = APIClient()
        self.client_3 = APIClient()
        self.client_unauthorized = APIClient()

        self.client.force_authenticate(user=self.user)
        self.client_2.force_authenticate(user=self.user_2)
        self.client_3.force_authenticate(user=self.user_no_account)

############### IMAGE LIST #################
    def test_image_list_view(self):
        url = reverse('image-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_image_list_view_2(self):
        url = reverse('image-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # one original image
        self.assertEqual(len(response.data[0]['thumbnails']), 2) # two thumbnail images

    def test_image_list_view_no_account(self):
        url = reverse('image-list')
        response = self.client_3.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_list_view_unauthorized(self):
        url = reverse('image-list')
        response = self.client_unauthorized.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

############### UPLOAD IMAGE #################
    def test_image_upload_view(self):
        url = reverse('image-upload')
        test_image = create_image(None, 'test.png')
        test_image_file = SimpleUploadedFile('test_file.png', test_image.getvalue())
        data = {'image': test_image_file}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['thumbnails']), 3)
        self.assertNotIn('expiring_link', response.data)

    def test_image_upload_view_expiring_link(self):
        url = reverse('image-upload')
        test_image = create_image(None, 'test.png')
        test_image_file = SimpleUploadedFile('test_file.png', test_image.getvalue())
        data = {'image': test_image_file, 'expiration': 500}
        response = self.client_2.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['thumbnails']), 2)
        self.assertEqual(response.data['expiring_link'][-3:], '500')

    def test_image_upload_view_fail(self):
        url = reverse('image-upload')
        invalid_image = 123
        data = {'image': invalid_image}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_list_view_no_account(self):
        url = reverse('image-upload')
        test_image = create_image(None, 'test.png')
        test_image_file = SimpleUploadedFile('test_file.png', test_image.getvalue())
        data = {'image': test_image_file, 'expiration': 500}
        response = self.client_3.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_list_view_unauthorized(self):
        url = reverse('image-upload')
        response = self.client_unauthorized.post(url, None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

############### EXPIRING LINK #################
    def test_image_expiring_link_view(self):
        unsigned_url = 'unigned_url'
        expiration_seconds = 400
        signed_url = signing.dumps(unsigned_url)
        signed_exp = signing.dumps(expiration_seconds)
        url = reverse('expiring_image', args=[signed_url, signed_exp])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_image_expiring_link_view_bad_signature(self):
        unsigned_url = 'unigned_url'
        unsigned_exp = 'unsigned_exp'
        url = reverse('expiring_image', args=[unsigned_url, unsigned_exp])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_expiring_link_view_missing_params(self):
        unsigned_exp = 'unsigned_exp'
        url = reverse('expiring_image', args=[None, unsigned_exp])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_expiring_link_view_unauthorized_should_work(self):
        unsigned_url = 'unigned_url'
        expiration_seconds = 400
        signed_url = signing.dumps(unsigned_url)
        signed_exp = signing.dumps(expiration_seconds)
        url = reverse('expiring_image', args=[signed_url, signed_exp])
        response = self.client_unauthorized.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
