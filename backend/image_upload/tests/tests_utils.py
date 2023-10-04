from PIL import Image as PILImage
from io import BytesIO

def create_image(storage, filename, size=(1, 1), image_mode='RGB', image_format='PNG'):
   data = BytesIO()
   PILImage.new(image_mode, size).save(data, image_format)
   data.seek(0)
   if not storage:
       return data
   image_file = ContentFile(data.read())
   return image_file
