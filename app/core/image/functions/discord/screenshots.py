import textwrap
from io import BytesIO
from typing import Union, BinaryIO

from PIL import ImageOps

from .models import ScreensShot


class DiscordMessageScreenShot(ScreensShot):

    DISCORD_BASE_COLOR = (54, 57, 62)

    FONT_SIZE = 15
    FONT_PADDING = (20, 0, 30, 3)
    FONT_PATH = ScreensShot.FONT_PATH + "whitney_discord.ttf"

    NAME_FONT_SIZE = 16
    NAME_FONT_PATH = ScreensShot.FONT_PATH + "whitney_bold_discord.ttf"

    TIME_STAMP_FONT_SIZE = 12
    TIME_STAMP_FONT_COLOR = (153, 170, 181)

    CONTENT_FONT_SIZE = 15
    CONTENT_WIDTH_SCALE = 100

    DISCORD_WIDTH_SCALE = 700
    BASE_PADDING = (20, 20, 60, 70)    # (left, top, right, bottom)

    AVATAR_SIZE = (40, 40)

    NAME_BOX_Y = BASE_PADDING[1]

    def __init__(self):
        self.discord_base: ScreensShot.Image.Image = None
        self.avatar: ScreensShot.Image.Image = None
        self.name: str = None
        self.content: str = None
        self.avatar: ScreensShot.Image.Image = None
        self.name_color: tuple = None
        self.time_stamp: str = None
        self.font = ScreensShot.ImageFont.truetype(self.FONT_PATH, self.FONT_SIZE)
        self.name_font = ScreensShot.ImageFont.truetype(self.NAME_FONT_PATH, self.NAME_FONT_SIZE)

    def _process(self):
        self.content = textwrap.wrap(self.content, self.CONTENT_WIDTH_SCALE, replace_whitespace=False)
        self.avatar = ScreensShot.Image.open(self.avatar)
        avatar_mask = ScreensShot.Image.new("L", self.avatar.size)
        avatar_drawer = ScreensShot.ImageDraw.Draw(avatar_mask)
        avatar_drawer.ellipse((0, 0) + self.avatar.size, fill=225)
        self.avatar.putalpha(avatar_mask)

        self.avatar: ScreensShot.Image.Image = ImageOps.fit(self.avatar, avatar_mask.size)
        self.avatar.putalpha(avatar_mask)
        self.avatar = self.avatar.resize(self.AVATAR_SIZE)

        if len(self.content) <= 2:
            self.FONT_PADDING = (20, 0, 50, 3)
        discord_base_x = self.DISCORD_WIDTH_SCALE+self.BASE_PADDING[0]+self.BASE_PADDING[2]
        discord_base_y = ((self.FONT_PADDING[2])*len(self.content))+self.BASE_PADDING[1]+self.BASE_PADDING[3]
        discord_base_size = (discord_base_x, discord_base_y)
        self.discord_base = ScreensShot.Image.new("RGB", discord_base_size, self.DISCORD_BASE_COLOR)
        if len(self.content) == 1:
            l, t, r, b = self.discord_base.getbbox()
            self.discord_base = self.discord_base.crop((l, t+30, r, b-30))
            self.NAME_BOX_Y = int((self.discord_base.size[1]-self.avatar.size[1])/2)
            avatar_xy = (self.BASE_PADDING[0], self.NAME_BOX_Y)
        else:
            avatar_xy = (self.BASE_PADDING[0], self.BASE_PADDING[1])
        self.discord_base.paste(self.avatar, avatar_xy, self.avatar)

        drawer = ScreensShot.ImageDraw.Draw(self.discord_base)

        name_xy = (self.BASE_PADDING[0] + self.AVATAR_SIZE[0] + self.FONT_PADDING[0], self.NAME_BOX_Y)
        drawer.text(name_xy, self.name, fill=self.name_color, font=self.name_font)

        _time_stamp_x = drawer.textsize(self.name, self.name_font)[0]
        time_stamp_xy = (_time_stamp_x+name_xy[0]+5, name_xy[1]+4.4)
        time_stamp_font = ScreensShot.ImageFont.truetype(self.FONT_PATH, self.TIME_STAMP_FONT_SIZE)
        drawer.text(time_stamp_xy, self.time_stamp, fill=self.TIME_STAMP_FONT_COLOR, font=time_stamp_font)

        content_xy = (name_xy[0], time_stamp_xy[1]+self.BASE_PADDING[1])
        content_y = content_xy[1]
        padding = self.FONT_PADDING[3]
        for line in self.content:
            w, h = drawer.textsize(line, font=self.font)
            drawer.text((content_xy[0], content_y), line, font=self.font)
            content_y += h + padding
        if len(self.content) != 1:
            l, t, r, b = self.discord_base.getbbox()
            b -= 20
            self.discord_base = self.discord_base.crop((l, t, r, b))

    def ss(self,
           name: str,
           message_content: str,
           avatar: Union[BytesIO, BinaryIO],
           name_color: tuple = (255, 255, 255),
           time_stamp: str = "Today at 11:38 AM"
           ):
        self.name = name
        self.content = message_content
        self.avatar = avatar
        self.name_color = name_color
        self.time_stamp = time_stamp
        self._process()
        return self.discord_base
