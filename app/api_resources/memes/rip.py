from ..base import ApiResourceBase
from flask import request, send_file, abort

from PIL import Image, ImageDraw, ImageFont


class RIP(ApiResourceBase):

    BASE_MEME_PATH = "app/api_resources/templates/misc/rip.png"

    AVATAR_SIZE = (128, 128)
    FONT_SIZE = 47

    AVATAR_PADDING = (10, 70)  # (LEFT, TOP)
    TEXT_PADDING = (10, 100)  # (LEFT, BOTTOM)

    FONT_PATH = ApiResourceBase.FONT_PATH + "OleoScript-Bold.ttf"

    def _process(self, *, text, avatar_url=None):
        base_meme = Image.open(self.BASE_MEME_PATH)
        if avatar_url:
            avatar = Image.open(self.get_image_from_url(avatar_url)).resize(self.AVATAR_SIZE)
            avatar_x = int((base_meme.size[0] - avatar.size[0]) / 2) - self.AVATAR_PADDING[0]
            avatar_y = self.AVATAR_PADDING[1] + int((base_meme.size[1] - avatar.size[1]) / 2)
            avatar_xy = (avatar_x, avatar_y, avatar.size[0] + avatar_x, avatar.size[1] + avatar_y)
            try:
                base_meme.paste(avatar, avatar_xy, avatar)
            except ValueError:
                base_meme.paste(avatar, avatar_xy)

        drawer = ImageDraw.Draw(base_meme)
        font = ImageFont.truetype(self.FONT_PATH, self.FONT_SIZE)
        text_width, text_height = drawer.textsize(text, font)
        text_x = (base_meme.size[0] - (text_width + self.TEXT_PADDING[0])) / 2
        text_y = base_meme.size[1] - (text_height + self.TEXT_PADDING[1])
        text_xy = (text_x, text_y)
        drawer.text(text_xy, text, fill=(0, 0, 0), font=font)
        return self.to_bytes(base_meme)

    ROUTE = "rip/"

    MEME_NAME = "rip.png"

    def post(self):
        payload = request.get_json()
        if payload is None:    # Browser or something.
            abort(400)
        if "text" not in payload or "avatar_url" not in payload:
            abort(400)
        meme_bytes, _ = self._process(**payload)
        return send_file(
            meme_bytes,
            mimetype="image/png",
            attachment_filename=self.MEME_NAME
        )
