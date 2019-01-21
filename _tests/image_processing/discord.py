import unittest

from PIL import Image

from typing import Union
from app.core.image.functions.discord.screenshots import DiscordMessageScreenShot


class MessageScreenshotsTest(unittest.TestCase):

    TEST_TEXT = "Test Test Test"
    TEST_IMAGE = open("_tests/image_processing/images/test1.gif", "rb")
    TEST_AVATAR_URL = "https://cdn.discordapp.com/avatars/331793750273687553/a_c59ddca1e44a4acb72654999459c58e0.gif"

    def test_message_screenshots(self):
        d = DiscordMessageScreenShot()
        d.content = self.TEST_TEXT
        d.avatar = self.TEST_IMAGE
        d.name = "The Cosmos"
        d.time_stamp = "Today at 11:38 AM"
        d._process()
        i = d.discord_base
        i.show()
        self.assertIsInstance(i, Union[Image.Image])
