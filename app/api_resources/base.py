import os
import base64
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

    ROUTE = str()

    def __new__(cls, *args, **kwargs):
        if not cls.ROUTE:
            raise NotImplementedError
        super().__init__(*args, **kwargs)

    IMAGE_CACHE_PATH = "cache/images/"
    FONT_PATH = "app/api_resources/templates/fonts/"

    MEDIA_MAX_SIZE = 4200000

    @staticmethod
    def encode_url(url):
        return base64.urlsafe_b64encode(url.encode("ascii")).decode("ascii")

    @staticmethod
    def get_image_from_url(url: str, max_size=MEDIA_MAX_SIZE):
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=max_size):
            if len(chunk) >= max_size:
                raise OverflowError
            image_bytes = BytesIO(chunk)
            image_bytes.seek(0)
            return image_bytes

    def get_cached_image_from_url(self, url: str, max_size=MEDIA_MAX_SIZE):
        file_path = self.IMAGE_CACHE_PATH + self.encode_url(url)
        try:
            with open(file_path, "rb") as file:
                return BytesIO(file.read())
        except FileNotFoundError:
            image_bytes = self.get_image_from_url(url, max_size)
            try:
                with open(file_path, "wb") as file:
                    file.write(image_bytes.read())
            except FileNotFoundError:
                os.makedirs(self.IMAGE_CACHE_PATH)
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
