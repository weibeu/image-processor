import os
import random

from flask import send_file
from flask_restful import Resource


class RandomEmote(Resource):

    BASE_PATH = "static/image/cache/emotes/"
    DIR_PATH = "app/core/server/static/image/cache/emotes"

    def __init__(self):
        self.name = str()
        self.__fetch_emote()

    @property
    def path(self):
        return self.BASE_PATH+self.name

    def __fetch_emote(self):
        emotes = os.listdir(self.DIR_PATH)
        self.name = random.choice(emotes)

    def get(self):
        return send_file(
            self.path,
            mimetype="image/png",
            attachment_filename=self.name
        )
