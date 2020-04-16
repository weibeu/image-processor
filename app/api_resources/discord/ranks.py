from flask import send_file
from ..base import ApiResourceBase
from PIL import Image, ImageDraw, ImageFont


class RankCard(ApiResourceBase):

    ROUTE = "profile/rank/"
    REQUIRED_DATA = [
        "name", "avatar_url", "discriminator", "text_rank", "voice_rank",
        "text_xp", "text_target_xp", "text_total_xp", "text_level",
        "voice_xp", "voice_target_xp", "voice_total_xp", "voice_level",
    ]

    NAME_FONT_PATH = ApiResourceBase.FONT_PATH + "KaushanScript-Regular.ttf"
    LEVEL_FONT_PATH = ApiResourceBase.FONT_PATH + "Merriweather-Bold.ttf"
    RANK_FONT_PATH = ApiResourceBase.FONT_PATH + "Futura_20Medium_20BT.ttf"
    TEXT_FONT_PATH = ApiResourceBase.FONT_PATH + "Futura_20Medium_20BT.ttf"
    DISCRIMINATOR_FONT_PATH = ApiResourceBase.FONT_PATH + "AmaticSC-Bold.ttf"

    RANK_CARD_BASE_PATH = ApiResourceBase.TEMPLATES_PATH + "discord/rank_card/rank_bg.png"
    LEVEL_MATERIAL_PATH = ApiResourceBase.TEMPLATES_PATH + "discord/rank_card/levelmaterial.png"

    AVATAR_SIZE = (553, 553)
    AVATAR_XY = (170, 299)
    # PROGRESS_CENTER = (2635, 299)

    LEVEL_MATERIAL_XY = (2413, 83)

    TEXT_PROGRESS_XY2 = [(2382, 52), (2874, 544)]
    TEXT_PROGRESS_XY1 = [(2330, 0), (2926, 596)]

    TEXT_PROGRESS_FILL2 = "#ff6859"
    TEXT_PROGRESS_FILL1 = "#ffcf44"
    # RANK_FILL1 = RANK_FILL2 = "#fc0e80"
    RANK_FILL1 = TEXT_PROGRESS_FILL1
    RANK_FILL2 = TEXT_PROGRESS_FILL2
    TEXT_FILL = "#1eb980"

    WIDTH_PROGRESS1 = 60
    WIDTH_PROGRESS2 = 50

    NAME_XY = (787, 417)
    LEVEL_XY1 = (2550, 90)    # (2573, 143)
    LEVEL_XY2 = (2550, 297)    # (2573, 370)
    RANK_XY1 = (1150, 660)    # (1920, 670)    # (1185, 770)    # (2300, 620)
    RANK_XY2 = (1150, 800)    # (2535, 670)    # (1185, 770)    # (2300, 620)
    TEXT_XP_XY = (1580, 897)
    TEXT_XP_TOTAL_XY = (1880 + 10, 897)
    VOICE_XP_XY = (2225, 897)
    VOICE_XP_TOTAL_XY = (2555 + 10, 897)

    def write_texts(self, kwargs, base):
        draw = ImageDraw.Draw(base)
        name_font = ImageFont.truetype(self.NAME_FONT_PATH, size=177)
        draw.text(self.NAME_XY, kwargs["name"], font=name_font)
        discriminator_xy = draw.textsize(kwargs["name"], font=name_font)
        discriminator_xy = discriminator_xy[0] + self.NAME_XY[0] + 10, self.NAME_XY[1] + discriminator_xy[1] - 90
        discriminator_font = ImageFont.truetype(self.DISCRIMINATOR_FONT_PATH, size=70)
        draw.text(discriminator_xy, kwargs["discriminator"], font=discriminator_font)

        level_font = ImageFont.truetype(self.LEVEL_FONT_PATH, size=147)
        draw.text(self.LEVEL_XY1, str(kwargs["text_level"]), fill=self.TEXT_PROGRESS_FILL1, font=level_font)
        draw.text(self.LEVEL_XY2, str(kwargs["voice_level"]), fill=self.TEXT_PROGRESS_FILL2, font=level_font)

        rank_font = ImageFont.truetype(self.RANK_FONT_PATH, size=150)
        draw.text(self.RANK_XY1, str(kwargs["text_rank"]), fill=self.RANK_FILL1, font=rank_font)
        draw.text(self.RANK_XY2, str(kwargs["voice_rank"]), fill=self.RANK_FILL2, font=rank_font)
        text_font = ImageFont.truetype(self.TEXT_FONT_PATH, size=53)
        draw.text(
            self.TEXT_XP_XY, f"{kwargs['text_xp']} / {kwargs['text_target_xp']}", fill=self.TEXT_FILL, font=text_font)
        draw.text(self.TEXT_XP_TOTAL_XY, str(kwargs["text_total_xp"]), fill=self.TEXT_FILL, font=text_font)
        draw.text(self.VOICE_XP_XY,
                  f"{kwargs['voice_xp']} / {kwargs['voice_target_xp']}", fill=self.TEXT_FILL, font=text_font)
        draw.text(self.VOICE_XP_TOTAL_XY, str(kwargs["voice_total_xp"]), fill=self.TEXT_FILL, font=text_font)

    def _process(self, **kwargs):
        base = Image.open(self.RANK_CARD_BASE_PATH)
        avatar = Image.open(self.get_image_from_url(kwargs["avatar_url"])).convert("RGBA")
        avatar = self.get_round_avatar(avatar)
        avatar = avatar.resize(self.AVATAR_SIZE)

        base.paste(avatar, self.AVATAR_XY, avatar)

        self.draw_circular_progress(
            base, kwargs["voice_xp"], kwargs["voice_target_xp"],
            self.TEXT_PROGRESS_XY2, width=self.WIDTH_PROGRESS2, fill=self.TEXT_PROGRESS_FILL2)

        self.draw_circular_progress(
            base, kwargs["text_xp"], kwargs["text_target_xp"],
            self.TEXT_PROGRESS_XY1, width=self.WIDTH_PROGRESS1, fill=self.TEXT_PROGRESS_FILL1)

        level_material = Image.open(self.LEVEL_MATERIAL_PATH)
        base.paste(level_material, self.LEVEL_MATERIAL_XY, level_material)

        self.write_texts(kwargs, base)

        return self.to_bytes(base)

    def post(self):
        payload = self.get_json()
        rank_card_bytes, _ = self._process(**payload)
        return send_file(
            rank_card_bytes, mimetype=f"image/{_}",
            attachment_filename=f"rank_card.{_}")
