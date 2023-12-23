from unittest.mock import patch, Mock, MagicMock

import pytest

from chalicelib.adapters.pillow_txt_to_initials_image_converter_adapter import (
    PillowTxtToInitialsImageConverterAdapter,
    TxtToInitialsImageConverterError,
)
from chalicelib.basic.basic_converter_adapter import BasicConverterAdapter
from chalicelib.domain.image_entity import ImageEntity
from chalicelib.domain.txt_entity import TxtEntity


def patcher(obj):
    prefix = (
        "chalicelib.adapters.pillow_txt_to_initials_image_converter_adapter"
    )

    return patch(f"{prefix}.{obj}")


class TestPillowTxtToInitialsImageConverterAdapter:
    @classmethod
    def setup_class(cls):
        cls.adapter = PillowTxtToInitialsImageConverterAdapter

    def test_parent(self):
        assert issubclass(self.adapter, BasicConverterAdapter)

    @patcher("BasicConverterAdapter.__init__")
    def test_init(self, mock_super_init):
        mock_logger = Mock()

        adapter = self.adapter(mock_logger)

        mock_super_init.assert_called_once_with(
            entity_cls_from=TxtEntity,
            entity_cls_to=ImageEntity,
            logger=mock_logger,
        )

        assert adapter.file_type_to == "png"

    @patcher("time")
    @patch.object(
        PillowTxtToInitialsImageConverterAdapter, "_make_image_bytes"
    )
    @patch.object(PillowTxtToInitialsImageConverterAdapter, "_make_image")
    def test_convert_successfully(
        self,
        mock_make_image,
        mock_make_image_bytes,
        _mock_time,
    ):
        _mock_logger = Mock()
        mock_txt = Mock()

        instance = self.adapter(_mock_logger)

        result = instance.convert(mock_txt)

        mock_txt.get_decoded_file_content.assert_called_once_with()

        mock_make_image_bytes.assert_called_once_with(
            mock_txt.get_decoded_file_content.return_value
        )

        mock_make_image.assert_called_once_with(
            mock_make_image_bytes.return_value,
            mock_txt.file_name,
            mock_txt.file_type,
        )

        assert result == mock_make_image.return_value

    @patcher("time")
    @patch.object(
        PillowTxtToInitialsImageConverterAdapter, "_make_image_bytes"
    )
    @patch.object(PillowTxtToInitialsImageConverterAdapter, "_make_image")
    def test_convert_raising_error(
        self,
        mock_make_image,
        mock_make_image_bytes,
        _mock_time,
    ):
        _mock_logger = Mock()
        mock_txt = Mock()

        instance = self.adapter(_mock_logger)

        mock_make_image.side_effect = Exception

        with pytest.raises(TxtToInitialsImageConverterError) as error:
            instance.convert(mock_txt)

        mock_txt.get_decoded_file_content.assert_called_once_with()

        mock_make_image_bytes.assert_called_once_with(
            mock_txt.get_decoded_file_content.return_value
        )

        mock_make_image.assert_called_once_with(
            mock_make_image_bytes.return_value,
            mock_txt.file_name,
            mock_txt.file_type,
        )

        assert str(error.value) == (
            f"Error converting {mock_txt.file_name} " "to png: Exception()"
        )

    @patch.object(
        PillowTxtToInitialsImageConverterAdapter, "_get_background_image"
    )
    @patch.object(PillowTxtToInitialsImageConverterAdapter, "_get_initials")
    @patch.object(
        PillowTxtToInitialsImageConverterAdapter, "_insert_text_on_image"
    )
    @patch.object(PillowTxtToInitialsImageConverterAdapter, "_get_image_bytes")
    def test_make_image_bytes(
        self,
        mock_get_image_bytes,
        mock_insert_text_on_image,
        mock_get_initials,
        mock_get_background_image,
    ):
        mock_file_content = Mock()

        instance = self.adapter()

        result = instance._make_image_bytes(mock_file_content)

        mock_get_background_image.assert_called_once_with()
        mock_get_initials.assert_called_once_with(mock_file_content)
        mock_insert_text_on_image.assert_called_once_with(
            mock_get_background_image.return_value,
            mock_get_initials.return_value,
        )

        mock_get_image_bytes.assert_called_once_with(
            mock_get_background_image.return_value
        )

        assert result == mock_get_image_bytes.return_value

    @patcher("BytesIO")
    def test_get_image_bytes(self, mock_bytes_io):
        mock_image = Mock()

        instance = self.adapter()

        result = instance._get_image_bytes(mock_image)

        mock_bytes_io.assert_called_once_with()
        mock_image.save.assert_called_once_with(
            mock_bytes_io.return_value, format=instance.file_type_to
        )

        assert result == mock_bytes_io.return_value

    @patcher("ImageDraw")
    @patch.object(PillowTxtToInitialsImageConverterAdapter, "_get_text_center")
    @patch.object(PillowTxtToInitialsImageConverterAdapter, "_get_font")
    def test_insert_text_on_image(
        self,
        mock_get_font,
        mock_get_text_center,
        mock_image_draw,
    ):
        mock_image = Mock()
        mock_initials = Mock()

        instance = self.adapter()

        instance._insert_text_on_image(mock_image, mock_initials)

        mock_image_draw.Draw.assert_called_once_with(mock_image)
        mock_get_font.assert_called_once_with()

        mock_font = mock_get_font.return_value
        mock_get_text_center.assert_called_once_with(
            mock_image_draw.Draw.return_value,
            mock_initials,
            mock_font,
        )

        mock_image_draw.Draw.return_value.text.assert_called_once_with(
            xy=mock_get_text_center.return_value,
            text=mock_initials,
            fill=(255, 255, 255),
            font=mock_font,
        )

    @patch.object(PillowTxtToInitialsImageConverterAdapter, "_get_bg_color")
    @patcher("Image")
    def test_get_background_image(
        self,
        mock_image,
        mock_get_bg_color,
    ):
        mock_logger = Mock()
        instance = self.adapter(mock_logger)

        result = instance._get_background_image()

        mock_get_bg_color.assert_called_once_with()
        mock_image.new.assert_called_once_with(
            mode="RGB",
            size=instance.DEFAULT_SIZE,
            color=mock_get_bg_color.return_value,
        )

        assert result == mock_image.new.return_value

    @patcher("random")
    def test_get_bg_color(self, mock_random):
        mock_logger = Mock()
        instance = self.adapter(mock_logger)

        result = instance._get_bg_color()

        mock_random.choice.assert_called_once_with(
            instance.POSSIBLE_BACKGROUNDS
        )

        assert result == mock_random.choice.return_value

    @patch.object(
        PillowTxtToInitialsImageConverterAdapter,
        "_get_valid_last_name_initial",
    )
    def test_get_initials_successfully(self, mock_get_valid_last_name_initial):
        mock_txt_file_content = Mock()
        mock_txt_file_content.split.return_value = ["C", "A"]
        mock_logger = Mock()
        instance = self.adapter(mock_logger)

        result = instance._get_initials(mock_txt_file_content)
        mock_get_valid_last_name_initial.assert_called_once_with("A")
        mock_txt_file_content.split.assert_called_once_with(" ")

        assert result == f"C{mock_get_valid_last_name_initial.return_value}"

    @patch.object(
        PillowTxtToInitialsImageConverterAdapter,
        "_get_valid_last_name_initial",
    )
    def test_get_initials_raising_error(
        self,
        mock_get_valid_last_name_initial,
    ):
        mock_txt_file_content = Mock()
        mock_txt_file_content.split.return_value = []
        mock_logger = Mock()
        instance = self.adapter(mock_logger)

        with pytest.raises(TxtToInitialsImageConverterError) as error:
            instance._get_initials(mock_txt_file_content)

        mock_get_valid_last_name_initial.assert_not_called()
        mock_txt_file_content.split.assert_called_once_with(" ")

        assert str(error.value) == (
            f"Error getting initials from {mock_txt_file_content}: "
            "IndexError(list index out of range)"
        )

    @patcher("Path")
    @patcher("ImageFont")
    def test_get_font(self, mock_image_font, mock_path):
        mock_logger = Mock()
        instance = self.adapter(mock_logger)

        result = instance._get_font()

        mock_path.return_value.parent.__truediv__.assert_called_once_with(
            "fonts"
        )
        mock_path.return_value.parent.__truediv__.return_value.__truediv__.assert_called_once_with(
            "arial_rounded.ttf"
        )
        mock_image_font.truetype.assert_called_once_with(
            font=str(
                mock_path.return_value.parent.__truediv__.return_value.__truediv__.return_value
            ),
            size=instance.DEFAULT_FONT_SIZE,
        )

        assert result == mock_image_font.truetype.return_value

    def test_get_text_center(self):
        mock_draw = Mock()
        mock_draw.textbbox.return_value = (0, 0, 0, 0)
        mock_initials = Mock()
        mock_font = Mock()

        mock_logger = Mock()

        instance = self.adapter(mock_logger)

        result = instance._get_text_center(mock_draw, mock_initials, mock_font)

        mock_draw.textbbox.assert_called_once_with(
            (0, 0), mock_initials, font=mock_font
        )

        assert result == (256.0, 256.0 - instance.DEFAULT_FONT_SIZE / 10)

    @patcher("ImageEntity")
    @patcher("Size")
    def test_make_image(self, mock_size, mock_image_entity):
        mock_image_bytes = Mock()
        mock_file_name = Mock()
        mock_file_type = Mock()

        mock_logger = Mock()

        instance = self.adapter(mock_logger)

        result = instance._make_image(
            mock_image_bytes, mock_file_name, mock_file_type
        )

        mock_file_name.replace.assert_called_once_with(
            mock_file_type, instance.file_type_to
        )

        mock_image_entity.assert_called_once_with(
            file_name=mock_file_name.replace.return_value,
            file_content=mock_image_entity.encode_image_bytes.return_value,
            file_type=instance.file_type_to,
            size=mock_size.return_value,
        )

        assert result == mock_image_entity.return_value

    def test_get_valid_last_name_initial_finding(self):
        mock_last_name = "UUUAZZ"
        mock_logger = Mock()
        instance = self.adapter(mock_logger)

        result = instance._get_valid_last_name_initial(mock_last_name)

        assert result == "A"

    def test_get_valid_last_name_initial_not_finding(self):
        mock_last_name = "UUUU"
        mock_logger = Mock()
        instance = self.adapter(mock_logger)

        result = instance._get_valid_last_name_initial(mock_last_name)

        assert result == "X"
