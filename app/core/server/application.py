from flask import Flask
from flask_restful import Api

from .api.resources.image_processor.memes import RIPMeme


app = Flask(__name__)
api = Api(app)

api.add_resource(RIPMeme, '/rip_meme/')
