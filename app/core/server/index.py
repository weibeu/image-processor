from flask import Flask, render_template
from flask_restful import Api

from .api.resources import RandomEmote


app = Flask(__name__)
api = Api(app)

api.add_resource(RandomEmote, '/random_emote/')


@app.route('/')
def index():
    return render_template("index.html")
