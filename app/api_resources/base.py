import os
import base64
import requests

from io import BytesIO
from PIL import Image, ImageDraw, ImageOps, ImageColor
from abc import abstractmethod

from flask import request, abort
from flask_restful import Resource


class ImageFunctions(object):

    @staticmethod
    def get_color(color):
        try:
            return ImageColor.getrgb(color)
        except (AttributeError, ValueError):
            return

    def add_avatar_border(self, avatar, width=10, outline=None):
        outline = self.get_color(outline or "#ffffff")
        drawer = ImageDraw.Draw(avatar)
        drawer.ellipse((0, 0) + avatar.size, width=width, outline=outline)
        return avatar

    @staticmethod
    def get_round_avatar(avatar):
        avatar_mask = Image.new("L", avatar.size)
        avatar_drawer = ImageDraw.Draw(avatar_mask)
        avatar_drawer.ellipse((0, 0) + avatar.size, fill=225)
        avatar = ImageOps.fit(avatar, avatar_mask.size)
        avatar.putalpha(avatar_mask)
        return avatar

    def draw_circular_progress(self, base, value, max_value, box, width=30, fill=None):
        fill = self.get_color(fill)
        angle = ((value / max_value) * 360) - 90
        drawer = ImageDraw.Draw(base)
        drawer.arc(box, -90, angle, width=width, fill=fill)


class ApiResourceBase(ImageFunctions, Resource):

    ROUTE = str()
    REQUIRED_DATA = list()

    TEMPLATES_PATH = "app/api_resources/templates/"

    def __new__(cls, *args, **kwargs):
        if not cls.ROUTE:
            raise NotImplementedError
        return super().__new__(cls, *args, **kwargs)

    IMAGE_CACHE_PATH = "cache/images/"
    FONT_PATH = "app/api_resources/templates/fonts/"

    MEDIA_MAX_SIZE = 4200000

    # Browser-like headers to avoid bot detection
    REQUEST_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    @staticmethod
    def encode_url(url):
        return base64.urlsafe_b64encode(url.encode("ascii")).decode("ascii")

    @staticmethod
    def get_image_from_url(url: str, max_size=MEDIA_MAX_SIZE):
        response = requests.get(url, headers=ApiResourceBase.REQUEST_HEADERS, stream=True, timeout=10)
        
        # Check for HTTP errors
        if response.status_code != 200:
            raise requests.HTTPError(f"HTTP {response.status_code} for URL: {url}")
        
        image_content = b""
        for chunk in response.iter_content(chunk_size=max_size):
            if len(chunk) >= max_size:
                raise OverflowError("Image size exceeds maximum allowed size")
            image_content += chunk
        
        # Validate that we got content
        if not image_content:
            raise ValueError(f"Empty response from URL: {url}")
        
        return BytesIO(image_content)

    def get_cached_image_from_url(self, url: str, max_size=MEDIA_MAX_SIZE):
        file_path = self.IMAGE_CACHE_PATH + self.encode_url(url)
        
        # Try to read from cache
        try:
            with open(file_path, "rb") as file:
                cached_content = file.read()
                # Validate cached file is not empty
                if cached_content:
                    return BytesIO(cached_content)
                else:
                    # Delete empty cache file
                    os.remove(file_path)
        except FileNotFoundError:
            pass
        
        # Download the image
        image_bytes = self.get_image_from_url(url, max_size)
        image_content = image_bytes.read()
        
        # Ensure cache directory exists
        os.makedirs(self.IMAGE_CACHE_PATH, exist_ok=True)
        
        # Write to cache
        with open(file_path, "wb") as file:
            file.write(image_content)
        
        # Return a new BytesIO with the content
        return BytesIO(image_content)

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

    def get_json(self):
        payload = request.get_json()
        if not all(key in payload for key in self.REQUIRED_DATA):
            abort(400)
        return payload
