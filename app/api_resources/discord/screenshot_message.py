import textwrap

from ..base import ApiResourceBase
from flask import send_file, request, abort

from PIL import Image, ImageDraw, ImageOps, ImageFont


class SSMessage(ApiResourceBase):

    DISCORD_BASE_COLOR = (54, 57, 62)

    FONT_SIZE = 15
    FONT_PADDING = (20, 0, 30, 3)
    FONT_PATH = ApiResourceBase.FONT_PATH + "whitney_discord.ttf"

    NAME_FONT_SIZE = 16
    NAME_FONT_PATH = ApiResourceBase.FONT_PATH + "whitney_bold_discord.ttf"

    TIME_STAMP_FONT_SIZE = 12
    TIME_STAMP_FONT_COLOR = (153, 170, 181)

    CONTENT_FONT_SIZE = 15
    CONTENT_WIDTH_SCALE = 100

    DISCORD_WIDTH_SCALE = 700
    BASE_PADDING = (20, 20, 60, 70)  # (left, top, right, bottom)

    AVATAR_SIZE = (40, 40)

    NAME_BOX_Y = BASE_PADDING[1]

    def _process(
            self, *, name, message_content, avatar_url, name_color=(255, 255, 255), time_stamp="Today at 11:38 AM"):
        content = textwrap.wrap(message_content, self.CONTENT_WIDTH_SCALE, replace_whitespace=False)
        avatar = Image.open(self.get_image_from_url(avatar_url))
        avatar_mask = Image.new("L", avatar.size)
        avatar_drawer = ImageDraw.Draw(avatar_mask)
        avatar_drawer.ellipse((0, 0) + avatar.size, fill=225)
        avatar.putalpha(avatar_mask)

        avatar = ImageOps.fit(avatar, avatar_mask.size)
        avatar.putalpha(avatar_mask)
        avatar = avatar.resize(self.AVATAR_SIZE)

        if len(content) <= 2:
            self.FONT_PADDING = (20, 0, 50, 3)
        discord_base_x = self.DISCORD_WIDTH_SCALE + self.BASE_PADDING[0] + self.BASE_PADDING[2]
        discord_base_y = ((self.FONT_PADDING[2]) * len(content)) + self.BASE_PADDING[1] + self.BASE_PADDING[3]
        discord_base_size = (discord_base_x, discord_base_y)
        discord_base = Image.new("RGB", discord_base_size, self.DISCORD_BASE_COLOR)
        if len(content) == 1:
            l, t, r, b = discord_base.getbbox()
            discord_base = discord_base.crop((l, t + 30, r, b - 30))
            self.NAME_BOX_Y = int((discord_base.size[1] - avatar.size[1]) / 2)
            avatar_xy = (self.BASE_PADDING[0], self.NAME_BOX_Y)
        else:
            avatar_xy = (self.BASE_PADDING[0], self.BASE_PADDING[1])
        discord_base.paste(avatar, avatar_xy, avatar)

        drawer = ImageDraw.Draw(discord_base)

        name_xy = (self.BASE_PADDING[0] + self.AVATAR_SIZE[0] + self.FONT_PADDING[0], self.NAME_BOX_Y)
        name_font = ImageFont.truetype(self.NAME_FONT_PATH, self.NAME_FONT_SIZE)
        drawer.text(name_xy, name, fill=name_color, font=name_font)

        _time_stamp_x = drawer.textsize(name, name_font)[0]
        time_stamp_xy = (_time_stamp_x + name_xy[0] + 5, name_xy[1] + 4.4)
        time_stamp_font = ImageFont.truetype(self.FONT_PATH, self.TIME_STAMP_FONT_SIZE)
        drawer.text(time_stamp_xy, time_stamp, fill=self.TIME_STAMP_FONT_COLOR, font=time_stamp_font)

        content_xy = (name_xy[0], time_stamp_xy[1] + self.BASE_PADDING[1])
        content_y = content_xy[1]
        padding = self.FONT_PADDING[3]
        font = ImageFont.truetype(self.FONT_PATH, self.FONT_SIZE)
        for line in content:
            w, h = drawer.textsize(line, font=font)
            drawer.text((content_xy[0], content_y), line, font=font)
            content_y += h + padding
        if len(content) != 1:
            l, t, r, b = discord_base.getbbox()
            b -= 20
            discord_base = discord_base.crop((l, t, r, b))

        return self.to_bytes(discord_base)

    ROUTE = "ss/message/"

    SS_NAME = "screen_shot.png"

    REQUIRED_DATA = [
        "name",
        "message_content",
        "avatar_url"
    ]

    BASE_DATA = REQUIRED_DATA + [
        "name_color",
        "time_stamp"
    ]

    def post(self):
        payload: dict = request.get_json()
        if payload is None:    # Browser or something.
            abort(400)
        if not all(key in payload for key in self.REQUIRED_DATA):
            abort(400)
        if "name_color" in payload:
            try:
                payload["name_color"] = tuple(payload.get("name_color"))
            except TypeError:
                payload.pop("name_color")

        if "time_stamp" in payload and payload["time_stamp"] is None:
            payload.pop("time_stamp")

        ss_bytes, _ = self._process(**payload)

        return send_file(
            ss_bytes,
            mimetype="image/png",
            download_name=self.SS_NAME
        )
