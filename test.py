import unittest
from typing import Union

from _tests.image_processing.memes import MemesTest
from _tests.image_processing.discord import MessageScreenshotsTest


if __name__ == "__main__":
    unittest.main(Union[MessageScreenshotsTest()])
    unittest.main(Union[MemesTest()])
