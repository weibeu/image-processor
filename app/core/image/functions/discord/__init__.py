from .screenshots import DiscordMessageScreenShot

from abc import ABC
from ..models import ProcessorABC

discord_msg_ss = DiscordMessageScreenShot()


class ScreenShotsProcessor(ProcessorABC, ABC):

    def ss_discord_msg(self, name: str,
                       message_content: str,
                       avatar_url: str,
                       name_color: tuple = (255, 255, 255),
                       time_stamp: str = "Today at 11:38 AM", *_, **__):
        avatar_bytes = self.image_from_url(avatar_url)
        ss = discord_msg_ss.ss(name, message_content, avatar_bytes, name_color, time_stamp)
        return self.get_image_bytes(ss)
