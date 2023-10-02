from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile
from django.core import signing

from image_upload.models import ThumbnailImage

def generate_thumbnail(image, size, id):
    with PILImage.open(image.image) as img:
        img.thumbnail((size, size))
        thumbnail_io = BytesIO()
        img.save(thumbnail_io, format='PNG')

        thumbnail_content = thumbnail_io.getvalue()
        thumbnail_name = f"image_{id}_size_{size}.png"
        return ContentFile(thumbnail_content, name=thumbnail_name)

def generate_thumbnails(image, account):
    thumbnail_urls = {}
    # Extracting thumbnail sizes from the string and converting to a list of integers
    thumbnail_sizes = [int(size.strip()) for size in account.tier.thumbnail_sizes.split(',') if size.strip()]

    for size in thumbnail_sizes:
        thumbnail_content = generate_thumbnail(image, size, image.id)

        thumbnail_image = ThumbnailImage.objects.create(
            original_image=image,
            thumbnail=thumbnail_content,
            thumbnail_size=size
        )
        thumbnail_urls[f"{size}px"] = thumbnail_image.thumbnail.url

    return thumbnail_urls


def sign_image_url(image_url, expiration_seconds):
    signed_url = signing.dumps(image_url)
    signed_exp = signing.dumps(expiration_seconds)

    signed_url_with_exp = f'{signed_url}/{signed_exp}?exp={expiration_seconds}'

    return signed_url_with_exp
