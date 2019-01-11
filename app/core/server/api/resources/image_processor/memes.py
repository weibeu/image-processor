import requests

from io import BytesIO

from flask import send_file, request, abort
from flask_restful import Resource

from app.core.image.processor import ImageProcessor


class RIPMeme(Resource):

    MEME_NAME = "rip.png"

    def get(self):
        payload = request.get_json()
        if payload is None:    # Browser or something.
            abort(400)
        text = payload.get("text")
        avatar_url = payload.get("avatar_url")
        raw_avatar = requests.get(avatar_url).content
        avatar_bytes = BytesIO(raw_avatar)
        meme = ImageProcessor().memes.rip.meme(text, avatar_bytes)
        meme_bytes = BytesIO()
        meme.save(meme_bytes, format="PNG")
        meme_bytes.seek(0)
        return send_file(
            meme_bytes,
            mimetype="image/png",
            attachment_filename=self.MEME_NAME
        )
