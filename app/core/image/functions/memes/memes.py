from PIL import Image, ImageDraw, ImageFont

from .models import Meme


class RIPMeme(Meme):

    BASE_MEME_PATH = "app/core/image/templates/misc/rip.png"
    TEXT_XY = (110, 333)

    FONT_PATH = Meme.FONT_PATH + "OleoScript-Bold.ttf"

    def __init__(self):
        self.base_meme = self.get_base_meme()
        self.text = str()
        self.avatar = None
        self.drawer = ImageDraw.Draw(self.base_meme)
        self.font = ImageFont.truetype(self.FONT_PATH, 50)

    def _process(self):
        self.drawer.text(self.TEXT_XY, self.text, fill=(0, 0, 0), font=self.font)

    def meme(self, text, avatar: Image = None) -> Image:
        self.text = text
        self.avatar = avatar
        self._process()
        return self.base_meme
