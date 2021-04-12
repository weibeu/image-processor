from ..base import ApiResourceBase
from flask import request, send_file, abort

from PIL import Image, ImageDraw, ImageFont


class Drake(ApiResourceBase):

    BASE_MEME_PATH = "app/api_resources/templates/memes/drake.jpg"
    FONT_PATH = ApiResourceBase.FONT_PATH + "Futura_20Medium_20BT.ttf"

    # COORDINATES: LEFT, TOP, RIGHT, BOTTOM.
    DRAKE_YES_BOX = (4005, 80, 7770, 3020)
    DRAKE_NO_BOX = (4005, 3180, 7770, 5400)

    FONT_SIZE = 700

    @staticmethod
    def _justify_center(outer_box, inner_box):
        outer_box_width = outer_box[2] - outer_box[0]
        outer_box_height = outer_box[3] - outer_box[1]
        inner_box_width = inner_box[2] - inner_box[0]
        inner_box_height = inner_box[3] - inner_box[1]
        x = (outer_box_width - inner_box_width) / 2
        y = (outer_box_height - inner_box_height) / 2
        return outer_box[0] + x, outer_box[1] + y

    def _process(self, drake_yes, drake_no):
        base_meme = Image.open(self.BASE_MEME_PATH)

        drawer = ImageDraw.Draw(base_meme)
        font = ImageFont.truetype(self.FONT_PATH, self.FONT_SIZE)

        content_width = self.DRAKE_YES_BOX[2] - self.DRAKE_YES_BOX[0]

        drake_yes_height, drake_yes_width = drawer.textsize(drake_yes, font=font)
        drake_no_height, drake_no_width = drawer.textsize(drake_no, font=font)

        if drake_yes_height < content_width:
            drake_yes_inner_box = (0, 0, drake_yes_width, drake_yes_height)
            drake_no_inner_box = (0, 0, drake_no_width, drake_no_height)
            drawer.text(self._justify_center(self.DRAKE_YES_BOX, drake_yes_inner_box), drake_yes, fill=(0, 0, 0), font=font)
            drawer.text(self._justify_center(self.DRAKE_NO_BOX, drake_no_inner_box), drake_no, fill=(0, 0, 0), font=font)

        return self.to_bytes(base_meme)

    ROUTE = "drake/"
    MEME_NAME = "drake.png"

    def post(self):
        payload = request.get_json()
        if payload is None:    # Browser or something.
            abort(400)
        if "drake_yes" not in payload and "drake_no" not in payload:
            abort(400)
        meme_bytes, _ = self._process(**payload)
        return send_file(
            meme_bytes,
            mimetype="image/png",
            attachment_filename=self.MEME_NAME
        )
