from unittest.mock import Mock

from chalicelib.interactors.convert_entity_interactor import (
    ConvertEntityInteractor,
)


class TestConvertEntityInteractor:
    @classmethod
    def setup_class(cls):
        cls.interactor = ConvertEntityInteractor

    def test_init(self):
        mock_converter_adapter = Mock()
        mock_request_body = Mock()

        instance = self.interactor(
            converter_adapter=mock_converter_adapter,
            request_body=mock_request_body,
        )

        assert instance.converter_adapter == mock_converter_adapter
        assert instance.request_body == mock_request_body

    def test_run(self):
        mock_converter_adapter = Mock()
        mock_request_body = Mock()

        instance = self.interactor(
            converter_adapter=mock_converter_adapter,
            request_body=mock_request_body,
        )

        result = instance.run()

        (
            mock_converter_adapter.entity_cls_from.from_json.assert_called_once_with(
                mock_request_body
            )
        )
        mock_entity = (
            mock_converter_adapter.entity_cls_from.from_json.return_value
        )

        mock_entity.set_converter_adapter.assert_called_once_with(
            mock_converter_adapter
        )

        mock_entity.convert.assert_called_once_with()
        mock_converted_entity = mock_entity.convert.return_value
        mock_converted_entity.to_json.assert_called_once_with()

        assert result == mock_converted_entity.to_json.return_value
