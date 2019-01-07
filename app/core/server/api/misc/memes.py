from flask import send_file
from flask_restful import Resource

from app.core.image.processor import ImageProcessor


class RIPMeme(Resource):

    MEME_NAME = "rip.png"
    FLASK_BASE_NAME = "static/image/cache/PIL/meme.png"
    BASE_NAME = "app/core/server/" + FLASK_BASE_NAME

    def get(self, text):
        meme = ImageProcessor().memes.rip.meme(text)
        meme.save(self.BASE_NAME)
        return send_file(
            self.FLASK_BASE_NAME,
            mimetype="image/png",
            attachment_filename=self.MEME_NAME
        )
