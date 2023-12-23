import random
from io import BytesIO
from pathlib import Path
from time import time

from PIL import Image, ImageDraw, ImageFont

from chalicelib.basic.basic_converter_adapter import BasicConverterAdapter
from chalicelib.domain.image_entity import Size
from chalicelib.domain.image_entity import ImageEntity
from chalicelib.domain.txt_entity import TxtEntity


class TxtToInitialsImageConverterError(Exception):
    pass


class PillowTxtToInitialsImageConverterAdapter(BasicConverterAdapter):
    DEFAULT_FONT_SIZE = 200
    DEFAULT_WIDTH = 512
    DEFAULT_HEIGHT = 512
    DEFAULT_SIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
    POSSIBLE_BACKGROUNDS = [
        (219, 173, 106),
        (235, 169, 136),
        (185, 192, 218),
    ]

    def __init__(self, logger=None, file_type_to="png"):
        super().__init__(
            entity_cls_from=TxtEntity, entity_cls_to=ImageEntity, logger=logger
        )
        self.file_type_to = file_type_to

    def convert(self, txt: TxtEntity) -> ImageEntity:
        file_name = txt.file_name
        file_type = txt.file_type

        try:
            file_content = txt.get_decoded_file_content()
            self.logger.info(
                f"Converting {str(txt)} to {self.file_type_to}..."
            )
            start = time()
            image_bytes = self._make_image_bytes(file_content)
            image = self._make_image(image_bytes, file_name, file_type)
            end = time()
            self.logger.info(
                f"Successfully converted {str(txt)} to "
                f"{self.file_type_to} ({str(image)})"
            )
            self.logger.info(f"Conversion took {end - start} seconds")
            return image
        except Exception as e:
            message = (
                f"Error converting {file_name} "
                f"to {self.file_type_to}: "
                f"{e.__class__.__name__}({e})"
            )
            self.logger.error(message)
            raise TxtToInitialsImageConverterError(message)

    def _make_image_bytes(self, txt_file_content):
        image = self._get_background_image()
        initials = self._get_initials(txt_file_content)
        self._insert_text_on_image(image, initials)
        return self._get_image_bytes(image)

    def _get_image_bytes(self, image):
        image_bytes = BytesIO()
        image.save(image_bytes, format=self.file_type_to)
        return image_bytes

    def _insert_text_on_image(self, image, initials):
        draw = ImageDraw.Draw(image)
        font = self._get_font()
        center = self._get_text_center(draw, initials, font)
        draw.textlength(initials, font=font)
        draw.text(
            xy=center,
            text=initials,
            fill=(255, 255, 255),
            font=font,
        )

    def _get_background_image(self):
        bg_color = self._get_bg_color()
        self.logger.info(f"Random background color: {bg_color}")
        image = Image.new(
            mode="RGB",
            size=self.DEFAULT_SIZE,
            color=bg_color,
        )
        return image

    def _get_bg_color(self):
        random_bg_color = random.choice(self.POSSIBLE_BACKGROUNDS)
        return random_bg_color

    def _get_initials(self, txt_file_content):
        try:
            splited = txt_file_content.split(" ")
            first_name = splited[0]
            last_name = splited[-1]
            first_name_initial = first_name[0].upper()
            last_name_initial = last_name[0].upper()

            if first_name_initial == "C":
                last_name_initial = self._get_valid_last_name_initial(
                    last_name
                )

            initials = f"{first_name_initial}{last_name_initial}"
            self.logger.info(f"Initials: {initials}")
        except Exception as e:
            message = (
                f"Error getting initials from {txt_file_content}: "
                f"{e.__class__.__name__}({e})"
            )
            self.logger.error(message)
            raise TxtToInitialsImageConverterError(message)

        return initials

    def _get_font(self):
        font_path = Path(__file__).parent / "fonts" / "arial_rounded.ttf"
        self.logger.info(f"Using font path: {font_path}")

        default_font = ImageFont.truetype(
            font=str(font_path), size=self.DEFAULT_FONT_SIZE
        )
        return default_font

    def _get_text_center(self, draw, initials, default_font):
        _, _, width, height = draw.textbbox(
            (0, 0), initials, font=default_font
        )
        image_width, image_height = self.DEFAULT_SIZE
        center_x = (image_width - width) / 2
        center_y = (image_height - height) / 2
        self.logger.info("Text was centered")
        return center_x, center_y - (self.DEFAULT_FONT_SIZE / 10)

    def _make_image(self, image_bytes, file_name, file_type):
        return ImageEntity(
            file_name=file_name.replace(file_type, self.file_type_to),
            file_content=ImageEntity.encode_image_bytes(
                image_bytes.getvalue()
            ),
            file_type=self.file_type_to,
            size=Size(
                width=self.DEFAULT_WIDTH,
                height=self.DEFAULT_HEIGHT,
            ),
        )

    @staticmethod
    def _get_valid_last_name_initial(last_name):
        invalid_last_name_initial = "U"

        for char in last_name:
            upper_char = char.upper()
            if upper_char != invalid_last_name_initial:
                return upper_char

        return "X"
