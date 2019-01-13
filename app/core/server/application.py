from flask import Flask
from flask_restful import Api

from .api.resources.image_processor import memes


app = Flask(__name__)
api = Api(app)

resources_packages = [
    memes
]

for resource_package in resources_packages:
    try:
        resource_package.setup(api)
    except AttributeError:
        print(f"[IGNORING {resource_package}]. Package does not have setup function.")
