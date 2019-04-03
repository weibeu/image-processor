import unittest

from PIL import Image

from typing import Union
from app.core.image.functions.discord.screenshots import DiscordMessageScreenShot
from app.core.image.functions.discord.banners import WelcomeBanner


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
        # i.show()
        self.assertIsInstance(i, Union[Image.Image])


class BannerTest(unittest.TestCase):

    BANNER = open("_tests/image_processing/images/banner.gif", "rb")
    AVATAR = open("_tests/image_processing/images/pfp.jpg", "rb")
    NAME = "The Cosmos#9806"
    TEXT = "Welcome to The Anime Discord! Make New friends! Enjoy your stay!"

    def test_welcome_banner(self):
        processor = WelcomeBanner()
        banner = processor._process(self.BANNER, self.AVATAR, self.NAME, self.TEXT)
        if isinstance(banner, list):
            banner[0].show()
            # banner[0].save("/home/thecosmos/Desktop/banner.png")
            # banner[0].save("/home/thecosmos/Desktop/banner.gif", save_all=True, append_images=banner[1:])
            self.assertIsInstance(banner[0], Union[Image.Image])
        else:
            # banner.show()
            # banner.save("/home/thecosmos/Desktop/banner.png")
            self.assertIsInstance(banner, Union[Image.Image])
