import flask_restful
from flask import send_file, request, abort
from flask_restful import Resource

from app.core.image.processor import ImageProcessor


image = ImageProcessor()


class RIPMeme(Resource):

    ROUTES = (
        "/memes/rip/",
    )

    MEME_NAME = "rip.png"

    def post(self):
        payload = request.get_json()
        if payload is None:    # Browser or something.
            abort(400)
        if "text" not in payload or "avatar_url" not in payload:
            abort(400)
        text = payload.get("text")
        avatar_url = payload.get("avatar_url")
        meme_bytes, _ = image.rip_meme(text, avatar_url)
        return send_file(
            meme_bytes,
            mimetype="image/png",
            attachment_filename=self.MEME_NAME
        )


resources = [
    RIPMeme
]


def setup(api: flask_restful.Api):
    for resource in resources:
        api.add_resource(resource, *resource.ROUTES)
