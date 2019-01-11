import unittest

from PIL import Image

from typing import Union
from app.core.image.functions.memes.memes import RIPMeme


class MemesTest(unittest.TestCase):

    TEST_TEXT = "Test Test Test"
    TEST_IMAGE = open("tests/image_processing/images/test1.gif", "rb")

    def test_rip_meme(self):
        rip_meme = RIPMeme()
        meme = rip_meme.meme(self.TEST_TEXT, self.TEST_IMAGE)
        # meme.show()
        self.assertIsInstance(meme, Union[Image.Image])
