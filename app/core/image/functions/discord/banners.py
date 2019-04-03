from PIL import ImageSequence

from .models import ImageFunction


class WelcomeBanner(ImageFunction):

    BANNER_AVATAR_RATIO = 2
    AVATAR_RATIO_Y = 17

    FONT_PATH = ImageFunction.FONT_PATH + "Bangers-Regular.ttf"
    NAME_FONT_SIZE_RATIO_XY = (11, 5)
    BANNER_NAME_RATIO = 1.68    # .537

    TEXT_FONT_PATH = ImageFunction.FONT_PATH + "Philosopher-Regular.ttf"
    TEXT_FONT_SIZE_RATIO_XY = (22, 9.8)
    BANNER_TEXT_RATIO = 1.222

    @staticmethod
    def __get_relative_font_size(xy, ratio_xy):
        x, y = xy
        font_size_x = int(x / ratio_xy[0])
        font_size_y = int(y / ratio_xy[1])
        # return font_size_y
        return min((font_size_x, font_size_y))

    def __write_text(self, base, name, text):
        draw = ImageFunction.ImageDraw.Draw(base)
        name_font_size = self.__get_relative_font_size(base.size, self.NAME_FONT_SIZE_RATIO_XY)
        name_font = ImageFunction.ImageFont.truetype(self.FONT_PATH, name_font_size)
        name_width, _ = draw.textsize(name, font=name_font)
        name_xy = (int((base.size[0] - name_width) / 2), int(base.size[1]/self.BANNER_NAME_RATIO))
        draw.text(name_xy, name, (255, 255, 255), font=name_font)
        text_font_size = self.__get_relative_font_size(base.size, self.TEXT_FONT_SIZE_RATIO_XY)
        text_font = ImageFunction.ImageFont.truetype(self.TEXT_FONT_PATH, text_font_size)
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

        avatar_xy = ((x - avatar.size[0]) // 2, y // self.AVATAR_RATIO_Y)
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
