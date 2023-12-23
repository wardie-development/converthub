from unittest.mock import patch, Mock, MagicMock

from chalicelib.basic.basic_file_entity import BasicFileEntity
from chalicelib.domain.image_entity import ImageEntity, Size


def patcher(obj):
    prefix = "chalicelib.domain.image_entity"

    return patch(f"{prefix}.{obj}")


class TestSize:
    @classmethod
    def setup_class(cls):
        cls.size = Size

    def test_from_json(self):
        mock_json_data = {
            "width": 1,
            "height": 2,
        }

        size = self.size.from_json(mock_json_data)

        assert size.width == mock_json_data["width"]
        assert size.height == mock_json_data["height"]

    def test_to_json(self):
        mock_width = 1
        mock_height = 2

        size = self.size(
            width=mock_width,
            height=mock_height,
        )

        json_data = size.to_json()

        assert json_data["width"] == mock_width
        assert json_data["height"] == mock_height


class TestImageEntity:
    @classmethod
    def setup_class(cls):
        cls.entity = ImageEntity

    def test_parent(self):
        assert issubclass(self.entity, BasicFileEntity)

    @patch.object(BasicFileEntity, "__init__")
    def test_init(self, mock_super_init):
        mock_file_content = Mock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_size = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            size=mock_size,
        )

        mock_super_init.assert_called_once_with(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
        )
        assert entity.size == mock_size
        assert entity.resize_adapter is None

    def test_set_resize_adapter(self):
        mock_file_content = Mock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_size = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            size=mock_size,
        )

        mock_resize_adapter = Mock()

        assert entity.resize_adapter is None
        entity.set_resize_adapter(mock_resize_adapter)
        assert entity.resize_adapter == mock_resize_adapter

    def test_resize(self):
        mock_file_content = Mock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_size = Mock()
        mock_resize_adapter = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            size=mock_size,
        )
        entity.resize_adapter = mock_resize_adapter

        mock_sizes = Mock()

        result = entity.resize(mock_sizes)

        mock_resize_adapter.resize.assert_called_once_with(entity, mock_sizes)

        assert result == mock_resize_adapter.resize.return_value

    @patcher("super")
    def test_to_json(self, mock_super):
        mock_file_content = Mock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_size = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            size=mock_size,
        )

        result = entity.to_json()

        mock_super.return_value.to_json.assert_called_once_with()
        mock_size.to_json.assert_called_once_with()

        assert result == {
            **mock_super.return_value.to_json.return_value,
            "size": mock_size.to_json.return_value,
        }

    @patcher("BytesIO")
    @patcher("base64.b64decode")
    def test_get_decoded_file_content(self, mock_b64decode, mock_bytesio):
        mock_file_content = Mock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_size = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            size=mock_size,
        )

        result = entity.get_decoded_file_content()

        mock_b64decode.assert_called_once_with(mock_file_content)
        mock_bytesio.assert_called_once_with(mock_b64decode.return_value)

        assert result == mock_bytesio.return_value

    @patcher("base64.b64encode")
    def test_encode_image_bytes(self, mock_b64encode):
        mock_image_bytes = Mock()

        result = self.entity.encode_image_bytes(mock_image_bytes)

        mock_b64encode.assert_called_once_with(mock_image_bytes)
        mock_b64encode.return_value.decode.assert_called_once_with("utf-8")

        assert result == mock_b64encode.return_value.decode.return_value

    def test_repr(self):
        mock_file_content = MagicMock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_size = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            size=mock_size,
        )

        result = repr(entity)

        assert result == (
            f"{self.entity.__name__}"
            f"(entity_id={entity.entity_id}, "
            f"file_name={entity.file_name}, "
            f"file_content={entity.file_content[:10]}, "
            f"file_type={entity.file_type}, "
            f"size={entity.size})"
        )
