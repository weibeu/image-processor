from io import BytesIO
from typing import Union

from typing.io import BinaryIO

from .models import Meme


class RIPMeme(Meme):

    BASE_MEME_PATH = "app/core/image/templates/misc/rip.png"

    AVATAR_SIZE = (128, 128)
    FONT_SIZE = 47

    AVATAR_PADDING = (10, 70)    # (LEFT, TOP)
    TEXT_PADDING = (10, 100)    # (LEFT, BOTTOM)

    FONT_PATH = Meme.FONT_PATH + "OleoScript-Bold.ttf"

    def __init__(self):
        self.base_meme = self.get_base_meme()
        self.text = str()
        self.avatar: Meme.Image.Image = None
        self.drawer = Meme.ImageDraw.Draw(self.base_meme)
        self.font = Meme.ImageFont.truetype(self.FONT_PATH, self.FONT_SIZE)

    def _process(self):
        if self.avatar is not None:
            self.avatar = Meme.Image.open(self.avatar).resize(self.AVATAR_SIZE)
            avatar_x = int((self.base_meme.size[0]-self.avatar.size[0])/2)-self.AVATAR_PADDING[0]
            avatar_y = self.AVATAR_PADDING[1]+int((self.base_meme.size[1]-self.avatar.size[1])/2)
            avatar_xy = (avatar_x, avatar_y, self.avatar.size[0]+avatar_x, self.avatar.size[1]+avatar_y)
            self.base_meme.paste(self.avatar, avatar_xy)

        text_width, text_height = self.drawer.textsize(self.text, self.font)
        text_x = (self.base_meme.size[0]-(text_width+self.TEXT_PADDING[0]))/2
        text_y = self.base_meme.size[1]-(text_height+self.TEXT_PADDING[1])
        text_xy = (text_x, text_y)
        self.drawer.text(text_xy, self.text, fill=(0, 0, 0), font=self.font)

    def meme(self, text, avatar: Union[BytesIO, BinaryIO] = None) -> Meme.Image.Image:
        self.text = text
        self.avatar = avatar
        self._process()
        return self.base_meme
