import unittest
import requests


class MemesTest(unittest.TestCase):

    URL = "http://127.0.0.1:5000/memes/rip/"

    TEXT = "Test Test Test"
    AVATAR_URL = "https://i.imgur.com/zsfY16f.jpg"

    def test_rip_meme(self):
        _bytes = requests.post(self.URL, json={
            "text": self.TEXT,
            "avatar_url": self.AVATAR_URL,
        }).content
        with open("results/meme.png", "wb") as file:
            file.write(_bytes)
        self.assertIsInstance(_bytes, bytes)

