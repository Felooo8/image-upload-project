from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list

# Create your models here.

class Tier(models.Model):
    """
    Defines different account tiers with properties like name, thumbnail sizes, link to the original image, and expiring link availability.

    Fields:
        name (str): Represents the name of the tier.
        thumbnail_sizes (str): Represents a comma-separated string of thumbnail sizes.
        link_to_original (bool): Indicates whether the tier allows linking to the original image.
        expiring_link (bool): Indicates whether the tier supports generating expiring links.
    """
    name = models.CharField(max_length=100)
    thumbnail_sizes = models.CharField(validators=[validate_comma_separated_integer_list], max_length=255)   
    link_to_original = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Account(models.Model):
    """"
    Associates a user with a specific account tier.

    Fields:
        user (User): Represents the associated user.
        tier (Tier): Represents the associated account tier.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Account for {self.user.username}"

class Image(models.Model):
    """
    Represents an uploaded image by a user, storing the image file and upload timestamp.

    Fields:
        user (User): Represents the user who uploaded the image.
        image (Image): Represents the uploaded image file.
        upload_timestamp (datetime): Represents the timestamp when the image was uploaded.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    upload_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"

class ThumbnailImage(models.Model):
    """
    Stores thumbnails of the original images with their respective sizes.

    Fields:
        original_image (Image): Represents the original image for which the thumbnail is generated.
        thumbnail (Image): Represents the thumbnail image file.
        thumbnail_size (int): Represents the size of the thumbnail.
    """
    original_image = models.ForeignKey(Image, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    thumbnail_size = models.PositiveIntegerField()

    def __str__(self):
        return f"Thumbnail for {self.original_image} - Size: {self.thumbnail_size}"
