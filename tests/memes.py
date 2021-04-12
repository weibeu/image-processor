import unittest
import requests


def save_file(bytes_, path):
    with open(path, "wb") as file:
        file.write(bytes_)


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

    def test_drake_meme(self):
        _bytes = requests.post("http://127.0.0.1:5000/memes/drake/", json={
            "drake_yes": "Schoool",
            "drake_no": "College",
        }).content
        save_file(_bytes, "results/drake.png")
        self.assertIsInstance(_bytes, bytes)
