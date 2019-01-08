from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from .models import Meme


class RIPMeme(Meme):

    BASE_MEME_PATH = "app/core/image/templates/misc/rip.png"
    TEXT_XY = (100, 450)
    AVATAR_BOX = (150, 300, 278, 428)

    FONT_PATH = Meme.FONT_PATH + "OleoScript-Bold.ttf"

    def __init__(self):
        self.base_meme = self.get_base_meme()
        self.text = str()
        self.avatar = None
        self.drawer = ImageDraw.Draw(self.base_meme)
        self.font = ImageFont.truetype(self.FONT_PATH, 50)

    def _process(self):
        if self.avatar is not None:
            self.avatar = Image.open(self.avatar)
            self.avatar.resize((200, 200))
            self.base_meme.paste(self.avatar, self.AVATAR_BOX)

        self.drawer.text(self.TEXT_XY, self.text, fill=(0, 0, 0), font=self.font)

    def meme(self, text, avatar: BytesIO = None) -> Image:
        self.text = text
        self.avatar = avatar
        self._process()
        return self.base_meme
