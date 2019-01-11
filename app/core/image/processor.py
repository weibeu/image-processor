from io import BytesIO

import requests
from PIL import Image
from .functions.memes import MemesProcessor


class ImageProcessor(MemesProcessor):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_image_bytes(image: Image.Image, image_format: str = "PNG"):
        image_bytes = BytesIO()
        image.save(image_bytes, format=image_format)
        image_bytes.seek(0)
        return image_bytes

    @staticmethod
    def image_from_url(url: str):
        response = requests.get(url)
        image_bytes = BytesIO(response.content)
        return image_bytes

    def rip_meme(self, text: str, avatar_url: str) -> BytesIO:
        avatar_bytes = self.image_from_url(avatar_url)
        meme = self.rip.meme(text, avatar_bytes)
        return self.get_image_bytes(meme)
