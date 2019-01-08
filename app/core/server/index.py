from flask import Flask, render_template
from flask_restful import Api

from .api.misc.memes import RIPMeme
from .api.resources import RandomEmote


app = Flask(__name__)
api = Api(app)

api.add_resource(RandomEmote, '/random_emote/')
api.add_resource(RIPMeme, '/rip_meme/<string:text>/<path:avatar_url>/')


@app.route('/')
def index():
    return render_template("index.html")
