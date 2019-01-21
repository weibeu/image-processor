from abc import ABC, abstractmethod
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont


class ProcessorABC(ABC):

    @staticmethod
    def get_image_bytes(image: Image.Image, image_format: str = "PNG"):
        image_bytes = BytesIO()
        image.save(image_bytes, format=image_format, optimize=True)
        image_bytes.seek(0)
        return image_bytes

    @staticmethod
    def image_from_url(url: str):
        response = requests.get(url)
        image_bytes = BytesIO(response.content)
        image_bytes.seek(0)
        return image_bytes


class ImageFunction(ProcessorABC, ABC):

    Image = Image
    ImageDraw = ImageDraw
    ImageFont = ImageFont

    FONT_PATH = "app/core/image/templates/fonts/"

    @abstractmethod
    def _process(self):
        raise NotImplementedError
