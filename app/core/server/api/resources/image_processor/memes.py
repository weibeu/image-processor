import requests

from io import BytesIO

from flask import send_file, request, abort
from flask_restful import Resource

from app.core.image.processor import ImageProcessor


class RIPMeme(Resource):

    MEME_NAME = "rip.png"

    def post(self):
        payload = request.get_json()
        if payload is None:    # Browser or something.
            abort(400)
        if "text" not in payload or "avatar_url" not in payload:
            abort(400)
        text = payload.get("text")
        avatar_url = payload.get("avatar_url")
        image = ImageProcessor()
        meme_bytes = image.rip_meme(text, avatar_url)
        return send_file(
            meme_bytes,
            mimetype="image/png",
            attachment_filename=self.MEME_NAME
        )
