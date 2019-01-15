from io import BytesIO

from app.core.image.functions.models import ProcessorABC
from .functions.memes import MemesProcessor
from .functions.discord import ScreenShotsProcessor


class ImageProcessor(MemesProcessor, ScreenShotsProcessor, ProcessorABC):

    def __init__(self):
        super().__init__()

    def rip_meme(self, text: str, avatar_url: str) -> BytesIO:
        avatar_bytes = self.image_from_url(avatar_url)
        meme = self.rip.meme(text, avatar_bytes)
        return self.get_image_bytes(meme)
