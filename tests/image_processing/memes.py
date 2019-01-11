import unittest

from PIL import Image

from typing import Union
from app.core.image.functions.memes.memes import RIPMeme
from app.core.image.processor import ImageProcessor


class MemesTest(unittest.TestCase):

    TEST_TEXT = "Test Test Test"
    TEST_IMAGE = open("tests/image_processing/images/test1.gif", "rb")
    TEST_AVATAR_URL = "https://cdn.discordapp.com/avatars/331793750273687553/a_c59ddca1e44a4acb72654999459c58e0.gif"

    def test_rip_meme(self):
        rip_meme = RIPMeme()
        meme = rip_meme.meme(self.TEST_TEXT, self.TEST_IMAGE)
        # meme.show()
        self.assertIsInstance(meme, Union[Image.Image])

    def test_rip_meme_model(self):
        image = ImageProcessor()
        meme = image.rip_meme(self.TEST_TEXT, self.TEST_AVATAR_URL)
        meme_image = Image.open(meme)
        # meme_image.show()
        self.assertIsInstance(meme_image, Union[Image.Image])
