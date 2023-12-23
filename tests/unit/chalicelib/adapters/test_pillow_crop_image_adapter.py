import pytest
from unittest.mock import patch, Mock, call, MagicMock

from chalicelib.adapters.pillow_resize_image_adapter import (
    PillowResizeImageAdapter,
    ResizeImageError,
)
from chalicelib.basic.basic_resize_image_adapter import BasicResizeImageAdapter


def patcher(obj):
    prefix = "chalicelib.adapters.pillow_resize_image_adapter"

    return patch(f"{prefix}.{obj}")


class TestPillowResizeImageAdapter:
    @classmethod
    def setup_class(cls):
        cls.adapter = PillowResizeImageAdapter

    def test_parent(self):
        assert issubclass(self.adapter, BasicResizeImageAdapter)

    @patch.object(BasicResizeImageAdapter, "__init__")
    def test_init(self, mock_super_init):
        mock_image = Mock
        mock_logger = Mock()

        self.adapter(mock_image, mock_logger)

        mock_super_init.assert_called_once_with(
            image_cls=mock_image, logger=mock_logger
        )

    @patcher("time")
    @patch.object(PillowResizeImageAdapter, "_resize_images")
    def test_resize(self, mock_resize_images, mock_time):
        mock_start = MagicMock()
        mock_end = MagicMock()

        mock_time.side_effect = [mock_start, mock_end]
        mock_image = Mock
        mock_logger = Mock()

        instance = self.adapter(mock_image, mock_logger)
        mock_entity_to_resize = Mock()
        mock_sizes = Mock()

        result = instance.resize(mock_entity_to_resize, mock_sizes)
        mock_logger.info.assert_has_calls(
            [
                call(f"Resizing image {mock_entity_to_resize}"),
                call("Resized images successfully"),
                call(
                    f"Resize took {mock_end.__sub__.return_value}" " seconds"
                ),
            ]
        )

        mock_end.__sub__.assert_called_once_with(mock_start)

        mock_resize_images.assert_called_once_with(
            mock_entity_to_resize, mock_sizes
        )

        assert result == mock_resize_images.return_value

    @patch.object(PillowResizeImageAdapter, "_resize_image")
    def test_resize_images(self, mock_resize_image):
        mock_image = Mock
        mock_logger = Mock()

        instance = self.adapter(mock_image, mock_logger)
        mock_entity_to_resize = Mock()
        mock_size = Mock()
        mock_sizes = [mock_size]

        result = instance._resize_images(mock_entity_to_resize, mock_sizes)

        mock_resize_image.assert_called_once_with(
            mock_entity_to_resize, mock_size
        )
        mock_logger.info.assert_called_once_with(
            f"Resized image {mock_resize_image.return_value}"
        )

        assert result == [mock_resize_image.return_value]

    @patcher("Image")
    @patcher("BytesIO")
    def test_resize_image_successfully(self, mock_bytesio, mock_image):
        mock_image_cls = Mock()
        mock_logger = Mock()

        instance = self.adapter(mock_image_cls, mock_logger)  # noqa

        mock_image_to_resize = Mock()
        mock_size = Mock()

        result = instance._resize_image(mock_image_to_resize, mock_size)

        mock_image_to_resize.get_decoded_file_content.assert_called_once_with()
        mock_image_content = (
            mock_image_to_resize.get_decoded_file_content.return_value
        )

        mock_image.open.assert_called_once_with(mock_image_content)
        mock_opened_image = mock_image.open.return_value

        mock_opened_image.resize.assert_called_once_with(
            (mock_size.width, mock_size.height)
        )
        mock_resized_image = mock_opened_image.resize.return_value
        mock_bytesio.assert_called_once_with()
        mock_resized_image.save.assert_called_once_with(
            mock_bytesio.return_value, format=mock_opened_image.format
        )
        mock_bytesio.return_value.getvalue.assert_called_once_with()
        mock_image_cls.encode_image_bytes.assert_called_once_with(
            mock_bytesio.return_value.getvalue.return_value
        )
        mock_opened_image.format.lower.assert_called_once_with()
        mock_image_cls.assert_called_once_with(
            file_content=mock_image_cls.encode_image_bytes.return_value,
            file_type=mock_opened_image.format.lower.return_value,
            file_name=(
                f"{mock_size.width}x{mock_size.height}_"
                f"{mock_image_to_resize.file_name}"
            ),
            size=mock_size,
        )

        assert result == mock_image_cls.return_value

    @patcher("Image")
    @patcher("BytesIO")
    def test_resize_image_raising_error(self, _mock_bytesio, _mock_image):
        mock_image_cls = Mock()
        mock_logger = Mock()

        instance = self.adapter(mock_image_cls, mock_logger)  # noqa

        error = Exception("error")
        mock_image_to_resize = Mock()
        mock_image_to_resize.get_decoded_file_content.side_effect = error
        mock_size = Mock()

        with pytest.raises(ResizeImageError) as error:
            instance._resize_image(mock_image_to_resize, mock_size)

        error_message = (
            f"Error resizing image {mock_image_to_resize}: " "Exception(error)"
        )

        mock_logger.error.assert_called_once_with(error_message)

        assert str(error.value) == error_message
