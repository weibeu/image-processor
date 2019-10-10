import flask_restful
from flask import Flask

from app.api_resources import discord, memes

resource_packages = [
    discord,
    # memes,
]


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    api = flask_restful.Api(app)

    if not config:
        app.config.from_object("configs")
    else:
        app.config.from_mapping(config)

    for resource_package in resource_packages:
        for resource in resource_package.RESOURCES:
            api.add_resource(resource, resource_package.BASE_ROUTE + resource.ROUTE)

    return app
