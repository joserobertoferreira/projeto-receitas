import os

from django.conf import settings
from PIL import Image


def resize_image(image, new_width=800):
    image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
    image_pillow = Image.open(image_full_path)
    original_width, original_height = image_pillow.size

    if original_width <= new_width:
        image_pillow.close()
        return

    resized_height = int((new_width * original_height) / original_width)

    new_image = image_pillow.resize((new_width, resized_height), Image.LANCZOS)  # noqa: W292

    new_image.save(
        image_full_path,
        optimize=True,
        quality=90,
    )
