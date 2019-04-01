from PIL import ImageSequence

from .models import ImageFunction


class WelcomeBanner(ImageFunction):

    BANNER_AVATAR_RATIO = 1.77
    AVATAR_PADDING = (0, 22, 0, 0)

    FONT_PATH = ImageFunction.FONT_PATH + "Bangers-Regular.ttf"
    NAME_FONT_SIZE = 70
    BANNER_NAME_RATIO = 1.537

    TEXT_FONT_PATH = ImageFunction.FONT_PATH + "Philosopher-Regular.ttf"
    TEXT_FONT_SIZE = 40
    BANNER_TEXT_RATIO = 1.2

    def __write_text(self, base, name, text):
        draw = ImageFunction.ImageDraw.Draw(base)
        name_font = ImageFunction.ImageFont.truetype(self.FONT_PATH, self.NAME_FONT_SIZE)
        name_width, _ = draw.textsize(name, font=name_font)
        name_xy = (int((base.size[0] - name_width) / 2), int(base.size[1]/self.BANNER_NAME_RATIO))
        draw.text(name_xy, name, (255, 255, 255), font=name_font)
        text_font = ImageFunction.ImageFont.truetype(self.TEXT_FONT_PATH, self.TEXT_FONT_SIZE)
        text_width, _ = draw.textsize(text, font=text_font)
        text_xy = (int((base.size[0] - text_width) / 2), int(base.size[1]/self.BANNER_TEXT_RATIO))
        draw.text(text_xy, text, fill=(255, 255, 255), font=text_font)
        return base

    def _process(self, banner, avatar, name, text, **kwargs):
        banner = ImageFunction.Image.open(banner)
        x, y = banner.size
        _ = int(y / self.BANNER_AVATAR_RATIO)
        avatar = ImageFunction.Image.open(avatar).resize((_, _))
        # avatar = self.add_avatar_border(avatar)
        avatar = self.get_avatar_icon(avatar)

        avatar_xy = ((x - avatar.size[0]) // 2, self.AVATAR_PADDING[1])
        frames = [f.copy() for f in ImageSequence.Iterator(banner)]

        if len(frames) == 1:
            banner.paste(avatar, avatar_xy, avatar)
            banner = self.__write_text(banner, name, text)
            frames = banner
        else:
            for i, frame in enumerate(frames):
                frame = frame.convert("RGBA")
                frame.paste(avatar, avatar_xy, avatar)
                frame = self.__write_text(frame, name, text)
                frames[i] = frame

        return frames

    def get_banner(self, *args, **kwargs):
        return self._process(*args, **kwargs)