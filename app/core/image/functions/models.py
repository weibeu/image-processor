from abc import ABC, abstractmethod
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps


class ProcessorABC(ABC):

    @staticmethod
    def get_image_bytes(image: Image.Image, image_format: str = "png"):
        image_bytes = BytesIO()
        if isinstance(image, list):
            image_format = "gif"
            image[0].save(image_bytes, save_all=True, append_images=image[1:], format=image_format.upper())
        else:
            image.save(image_bytes, format=image_format.upper())
        image_bytes.seek(0)
        return image_bytes, image_format

    @staticmethod
    def image_from_url(url: str, max_size=3145730):
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=max_size):
            if len(chunk) >= max_size:
                raise OverflowError
            image_bytes = BytesIO(chunk)
            image_bytes.seek(0)
            return image_bytes

    @staticmethod
    def get_avatar_icon(avatar):
        avatar_mask = Image.new("L", avatar.size)
        avatar_drawer = ImageDraw.Draw(avatar_mask)
        avatar_drawer.ellipse((0, 0) + avatar.size, fill=225)
        avatar = ImageOps.fit(avatar, avatar_mask.size)
        avatar.putalpha(avatar_mask)
        return avatar

    @staticmethod
    def add_avatar_border(avatar, width=10):
        drawer = ImageDraw.Draw(avatar)
        drawer.ellipse((0, 0) + avatar.size, width=width)
        return avatar

    @staticmethod
    def add_banner_border(banner, width=10):
        drawer = ImageDraw.Draw(banner)
        xy = (0, 0) + banner.size
        drawer.rectangle(xy, width=width)
        return banner


class ImageFunction(ProcessorABC, ABC):

    Image = Image
    ImageDraw = ImageDraw
    ImageFont = ImageFont

    FONT_PATH = "app/core/image/templates/fonts/"

    @abstractmethod
    def _process(self, *args, **kwargs):
        raise NotImplementedError
