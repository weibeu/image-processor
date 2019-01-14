from abc import ABC, abstractmethod

from ..models import ImageFunction
from PIL import Image


class Meme(ImageFunction, ABC):

    FONT_PATH = "app/core/image/templates/fonts/"

    @property
    @abstractmethod
    def BASE_MEME_PATH(self):
        raise NotImplementedError

    @abstractmethod
    def meme(self, text: str, avatar: Image) -> Image:
        raise NotImplementedError

    def get_base_meme(self) -> Image:
        return Image.open(self.BASE_MEME_PATH)
