from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list

# Create your models here.

class Tier(models.Model):
    name = models.CharField(max_length=100)
    thumbnail_sizes = models.CharField(validators=[validate_comma_separated_integer_list], max_length=255)   
    link_to_original = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, blank=True)

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    upload_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded by {self.user.username}"