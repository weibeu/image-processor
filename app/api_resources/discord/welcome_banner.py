from ..base import ApiResourceBase
from flask import request, send_file, abort

from PIL import Image, ImageSequence, ImageDraw, ImageOps, ImageFont, ImageColor


def add_banner_border(banner, width=10, outline=None):
    drawer = ImageDraw.Draw(banner)
    xy = (0, 0) + banner.size
    try:
        outline = ImageColor.getrgb(outline or "#ffffff")
    except ValueError:
        outline = None
    drawer.rectangle(xy, width=width, outline=outline)
    return banner


def get_relative_font_size(xy, ratio_xy):
    x, y = xy
    font_size_x = int(x / ratio_xy[0])
    font_size_y = int(y / ratio_xy[1])
    # return font_size_y
    return min((font_size_x, font_size_y))


class WelcomeBanner(ApiResourceBase):

    ROUTE = "banners/welcome/"

    REQUIRED_DATA = [
        "banner_url",
        "avatar_url",
        "name",
        "text",
    ]

    BANNER_AVATAR_RATIO = 2
    AVATAR_RATIO_Y = 17

    FONT_PATH = ApiResourceBase.FONT_PATH + "KaushanScript-Regular.ttf"
    NAME_FONT_SIZE_RATIO_XY = (11, 5)
    BANNER_NAME_RATIO = 1.77    # 1.67  # .537

    NAME_DISCRIMINATOR_PADDING = 1

    DISCRIMINATOR_FRONT_PATH = ApiResourceBase.FONT_PATH + "AmaticSC-Bold.ttf"
    DISCRIMINATOR_FRONT_SIZE_RATIO_XY = (NAME_FONT_SIZE_RATIO_XY[0] * 1.7, NAME_FONT_SIZE_RATIO_XY[1] * 1.7)
    BANNER_DISCRIMINATOR_RATIO = 1.50

    TEXT_FONT_PATH = ApiResourceBase.FONT_PATH + "Raleway-Regular.ttf"
    TEXT_FONT_SIZE_RATIO_XY = (25, 11)
    BANNER_TEXT_RATIO = 1.222

    BORDER_HEIGHT_RATIO = 70

    BASE_FILENAME = "welcome"

    DISCORD_BANNER_SIZE = (1080, 610)

    def write_text(self, base, payload):
        draw = ImageDraw.Draw(base)
        name_font_size = get_relative_font_size(base.size, self.NAME_FONT_SIZE_RATIO_XY)
        name_font = ImageFont.truetype(self.FONT_PATH, name_font_size)
        disc_font_size = get_relative_font_size(base.size, self.DISCRIMINATOR_FRONT_SIZE_RATIO_XY)
        disc_font = ImageFont.truetype(self.DISCRIMINATOR_FRONT_PATH, disc_font_size)
        name_width, _ = draw.textsize(payload["name"], font=name_font)
        disc_width, _ = draw.textsize(payload["discriminator"], font=disc_font)
        name_xy = (int((base.size[0] - (name_width + disc_width)) / 2), int(base.size[1] / self.BANNER_NAME_RATIO))
        disc_x = name_xy[0] + name_width + self.NAME_DISCRIMINATOR_PADDING
        disc_xy = (disc_x, int(base.size[1] / self.BANNER_DISCRIMINATOR_RATIO))
        draw.text(name_xy, payload["name"], fill=payload.get("font_color") or (255, 255, 255), font=name_font)
        draw.text(disc_xy, payload["discriminator"], fill=payload.get("font_color") or (255, 255, 255), font=disc_font)
        text_font_size = get_relative_font_size(base.size, self.TEXT_FONT_SIZE_RATIO_XY)
        text_font = ImageFont.truetype(self.TEXT_FONT_PATH, text_font_size)
        text_width, _ = draw.textsize(payload["text"], font=text_font)
        text_xy = (int((base.size[0] - text_width) / 2), int(base.size[1] / self.BANNER_TEXT_RATIO))
        draw.text(text_xy, payload["text"], fill=payload.get("font_color") or (255, 255, 255), font=text_font)
        return base

    def _process(self, **payload):
        banner = Image.open(self.get_cached_image_from_url(payload["banner_url"]))
        x, y = banner.size
        _x, _y = (self.DISCORD_BANNER_SIZE[0], int((x / y)) * self.DISCORD_BANNER_SIZE[1])
        _ = int(y / self.BANNER_AVATAR_RATIO)
        avatar = Image.open(self.get_image_from_url(payload["avatar_url"])).convert("RGBA")
        # avatar = self.add_avatar_border(avatar)
        avatar = self.get_round_avatar(avatar)

        border_width = y // self.BORDER_HEIGHT_RATIO

        avatar = avatar.resize((_, _))
        avatar = self.add_avatar_border(avatar, border_width, payload.get("border_color"))

        avatar_xy = ((x - avatar.size[0]) // 2, y // self.AVATAR_RATIO_Y)
        frames = [f.copy() for f in ImageSequence.Iterator(banner)]

        if len(frames) == 1:
            banner.paste(avatar, avatar_xy, avatar)
            banner = add_banner_border(banner, border_width, outline=payload.get("border_color"))
            banner = self.write_text(banner, payload)
            banner.thumbnail(self.DISCORD_BANNER_SIZE, Image.ANTIALIAS)
            frames = banner
        else:
            for i, frame in enumerate(frames):
                frame = frame.convert("RGBA")
                frame.paste(avatar, avatar_xy, avatar)
                frame = add_banner_border(frame, border_width, outline=payload.get("border_color"))
                frame = self.write_text(frame, payload)
                frame.thumbnail(self.DISCORD_BANNER_SIZE, Image.ANTIALIAS)
                frames[i] = frame

        return self.to_bytes(frames)

    def post(self):
        payload = self.get_json()

        try:
            banner_bytes, _ = self._process(**payload)
        except OverflowError:
            abort(413)
        else:
            return send_file(
                banner_bytes,
                mimetype=f"image/{_}",
                download_name=f"{self.BASE_FILENAME}.{_}"
            )
