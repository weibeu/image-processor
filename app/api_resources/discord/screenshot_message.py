import flask_restful

from flask_restful import Resource
from flask import send_file, request, abort


class SSDiscordMessage(Resource):

    ROUTES = (
        "discord/ss/message/",
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

        ss_bytes, _ = image.ss_discord_msg(**payload)

        return send_file(
            ss_bytes,
            mimetype="image/png",
            attachment_filename=self.SS_NAME
        )



resources = [
    SSDiscordMessage,
    DiscordWelcomeBanner,
]


def setup(api: flask_restful.Api):
    for resource in resources:
        api.add_resource(resource, *resource.ROUTES)
