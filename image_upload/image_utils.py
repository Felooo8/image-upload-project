from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile

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
    # Extracting thumbnail sizes from the string and converting to a list of integers
    thumbnail_sizes = [int(size.strip()) for size in account.tier.thumbnail_sizes.split(',') if size.strip()]

    for size in thumbnail_sizes:
        thumbnail_content = generate_thumbnail(image, size, image.id)

        ThumbnailImage.objects.create(
            original_image=image,
            thumbnail=thumbnail_content,
            thumbnail_size=size
        )
