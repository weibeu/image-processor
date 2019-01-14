from abc import ABC, abstractmethod

from PIL import Image, ImageDraw, ImageFont


class ImageFunction(ABC):

    Image = Image
    ImageDraw = ImageDraw
    ImageFont = ImageFont

    FONT_PATH = "app/core/image/templates/fonts/"

    @abstractmethod
    def _process(self):
        raise NotImplementedError
