import requests
from io import BytesIO
from PIL import Image, ImageDraw
from abc import abstractmethod

from flask_restful import Resource


class ImageFunctions(object):

    @staticmethod
    def add_avatar_border(avatar, width=10):
        drawer = ImageDraw.Draw(avatar)
        drawer.ellipse((0, 0) + avatar.size, width=width)
        return avatar


class ApiResourceBase(ImageFunctions, Resource):

    FONT_PATH = "app/api_resources/templates/fonts/"

    @staticmethod
    def get_image_from_url(url: str, max_size=3145730):
        # TODO: Implement local image cache.
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=max_size):
            if len(chunk) >= max_size:
                raise OverflowError
            image_bytes = BytesIO(chunk)
            image_bytes.seek(0)
            return image_bytes

    @abstractmethod
    def _process(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def to_bytes(image: Image.Image, image_format: str = "png"):
        image_bytes = BytesIO()
        if isinstance(image, list):
            image_format = "gif"
            image[0].save(
                image_bytes, save_all=True, append_images=image[1:], format=image_format.upper(), optimize=True)
        else:
            image.save(image_bytes, format=image_format.upper())
        image_bytes.seek(0)
        return image_bytes, image_format
