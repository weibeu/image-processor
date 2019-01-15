from . import memes
from . import discord

image_resource_packages = [
    memes,
    discord
]

for package in image_resource_packages:
    try:
        assert hasattr(package, "resources")
    except AssertionError:
        raise AssertionError
