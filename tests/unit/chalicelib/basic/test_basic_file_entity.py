from unittest.mock import Mock, patch, MagicMock

from chalicelib.basic.basic_file_entity import BasicFileEntity


def patcher(obj):
    prefix = "chalicelib.basic.basic_file_entity"

    return patch(f"{prefix}.{obj}")


class TestBasicFileEntity:
    @classmethod
    def setup_class(cls):
        cls.entity = BasicFileEntity

    def test_init(self):
        mock_file_content = Mock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_entity_id = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            entity_id=mock_entity_id,
        )

        assert entity.file_content == mock_file_content
        assert entity.file_type == mock_file_type
        assert entity.file_name == mock_file_name
        assert entity.entity_id == mock_entity_id

    def test_set_converter_adapter(self):
        mock_file_content = Mock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_entity_id = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            entity_id=mock_entity_id,
        )

        mock_converter_adapter = Mock()

        assert entity.converter_adapter is None
        entity.set_converter_adapter(mock_converter_adapter)
        assert entity.converter_adapter == mock_converter_adapter

    def test_convert(self):
        mock_file_content = Mock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_entity_id = Mock()
        mock_converter_adapter = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            entity_id=mock_entity_id,
        )
        entity.converter_adapter = mock_converter_adapter
        result = entity.convert()

        mock_converter_adapter.convert.assert_called_once_with(entity)

        assert result == mock_converter_adapter.convert.return_value

    def test_from_json(self):
        mock_json_data = {
            "file_content": Mock(),
            "file_type": Mock(),
            "file_name": Mock(),
            "entity_id": Mock(),
        }

        result = self.entity.from_json(mock_json_data)

        assert result == self.entity(**mock_json_data)

    def test_to_json(self):
        mock_file_content = Mock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_entity_id = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            entity_id=mock_entity_id,
        )

        result = entity.to_json()

        assert result == {
            "file_name": mock_file_name,
            "file_content": mock_file_content,
            "file_type": mock_file_type,
            "entity_id": mock_entity_id,
        }

    @patcher("base64.b64decode")
    def test_get_decoded_file_content(self, mock_b64decode):
        mock_file_content = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=Mock(),
            file_name=Mock(),
            entity_id=Mock(),
        )

        result = entity.get_decoded_file_content()

        mock_b64decode.assert_called_once_with(mock_file_content)
        mock_b64decode.return_value.decode.assert_called_once_with("utf-8")

        assert result == mock_b64decode.return_value.decode.return_value

    def test_eq(self):
        mock_entity_id = Mock()

        entity = self.entity(
            file_content=Mock(),
            file_type=Mock(),
            file_name=Mock(),
            entity_id=mock_entity_id,
        )

        mock_other = Mock()
        mock_other.entity_id = mock_entity_id

        assert entity == mock_other

    def test_repr(self):
        mock_file_content = MagicMock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_entity_id = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            entity_id=mock_entity_id,
        )

        result = entity.__repr__()

        assert result == (
            f"{self.entity.__name__}"
            f"(entity_id={mock_entity_id}, "
            f"file_name={mock_file_name}, "
            f"file_content={mock_file_content[:10]}, "
            f"file_type={mock_file_type})"
        )

    @patch.object(BasicFileEntity, "__repr__")
    def test_str(self, mock_repr):
        mock_repr.return_value = Mock()

        mock_file_content = MagicMock()
        mock_file_type = Mock()
        mock_file_name = Mock()
        mock_entity_id = Mock()

        entity = self.entity(
            file_content=mock_file_content,
            file_type=mock_file_type,
            file_name=mock_file_name,
            entity_id=mock_entity_id,
        )

        result = entity.__str__()
        mock_repr.assert_called_once_with()

        assert result == mock_repr.return_value
