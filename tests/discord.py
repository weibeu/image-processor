import unittest
import requests


class DiscordTestCase(unittest.TestCase):

    BASE_URL = "http://127.0.0.1:5000/discord"


class BannerTest(DiscordTestCase):

    PATH = "/banners/welcome/"
    URL = DiscordTestCase.BASE_URL + PATH

    A_BANNER_URL = "https://i.imgur.com/6aieR4Y.gif"
    BANNER_URL = "https://i.imgur.com/I8fNRV8.jpg"
    AVATAR_URL = "https://i.imgur.com/zsfY16f.jpg"

    NAME = "The Cosmos#7777"
    TEXT = "Welcome to B-20! Enjoy your stay!"

    def test_welcome_banner(self):
        _bytes = requests.post(self.URL, json={
            "banner_url": self.BANNER_URL,
            "avatar_url": self.AVATAR_URL,
            "name": self.NAME,
            "text": self.TEXT,
        }).content
        with open("results/test.png", "wb") as file:
            file.write(_bytes)
        self.assertIsInstance(_bytes, bytes)


class MessageScreenshotsTest(DiscordTestCase):

    PATH = "/ss/message/"
    URL = DiscordTestCase.BASE_URL + PATH

    NAME = "The Cosmos#9806"
    MESSAGE_CONTENT = "mply dummy text of the printing and typesetting industry. Lorem Ipsum has been the ind"
    TEST_URL = "https://i.imgur.com/zsfY16f.jpg"

    def test_message_screenshots(self):
        _bytes = requests.post(self.URL, json={
            "name": self.NAME,
            "message_content": self.MESSAGE_CONTENT,
            "avatar_url": self.TEST_URL,
        }).content
        with open("results/testss.png", "wb") as file:
            file.write(_bytes)
        self.assertIsInstance(_bytes, bytes)


class RankCardTest(DiscordTestCase):

    PATH = "/profile/rank/"
    URL = DiscordTestCase.BASE_URL + PATH

    def test_rank_card(self):
        _bytes = requests.post(self.URL, json={}).content
        with open("results/rank_card.png", "wb") as file:
            file.write(_bytes)
        self.assertIsInstance(_bytes, bytes)
