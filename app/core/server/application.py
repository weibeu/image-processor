from flask import Flask
from flask_restful import Api

from .api.resources.image_processor import image_resource_packages


app = Flask(__name__)
api = Api(app)


for resource_package in image_resource_packages:
    try:
        resource_package.setup(api)
    except AttributeError:
        print(f"[IGNORING {resource_package}]. Package does not have setup function.")
