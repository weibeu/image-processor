import flask_restful
from flask import send_file, request, abort
from flask_restful import Resource

from app.core.image.processor import ImageProcessor


image = ImageProcessor()


class SSDiscordMessage(Resource):

    ROUTES = (
        "/discord/ss/message/",
    )

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
        payload = request.get_json()
        if payload is None:    # Browser or something.
            abort(400)
        if not all(key in payload for key in self.REQUIRED_DATA):
            abort(400)

        ss_bytes = image.ss_discord_msg(**payload)

        return send_file(
            ss_bytes,
            mimetype="image/png",
            attachment_filename=self.SS_NAME
        )


resources = [
    SSDiscordMessage
]


def setup(api: flask_restful.Api):
    for resource in resources:
        api.add_resource(resource, *resource.ROUTES)
