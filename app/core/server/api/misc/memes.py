from io import BytesIO

import requests
from flask import send_file
from flask_restful import Resource

from app.core.image.processor import ImageProcessor


class RIPMeme(Resource):

    MEME_NAME = "rip.png"

    def get(self, text, avatar_url):
        response = requests.get(avatar_url)
        avatar_bytes = BytesIO(response.content)
        meme = ImageProcessor().memes.rip.meme(text, avatar_bytes)
        meme_bytes = BytesIO()
        meme.save(meme_bytes, format="PNG")
        meme_bytes.seek(0)
        return send_file(
            meme_bytes,
            mimetype="image/png",
            attachment_filename=self.MEME_NAME
        )
