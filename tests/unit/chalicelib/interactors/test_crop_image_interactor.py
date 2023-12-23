from unittest.mock import patch, Mock

from chalicelib.interactors.resize_image_interactor import (
    ResizeImageRequest,
    ResizeImageInteractor,
)


def patcher(obj):
    prefix = "chalicelib.interactors.resize_image_interactor"

    return patch(f"{prefix}.{obj}")


class TestResizeImageRequest:
    @classmethod
    def setup_class(cls):
        cls.request = ResizeImageRequest

    @patch.object(ResizeImageRequest, "_extract_sizes")
    def test_init(self, mock_extract_sizes):
        mock_request_body = Mock()

        instance = self.request(request_body=mock_request_body)

        mock_extract_sizes.assert_called_once_with(mock_request_body)

        assert instance.sizes == mock_extract_sizes.return_value
        assert instance.request_body == mock_request_body

    @patcher("Size")
    def test_extract_sizes(self, mock_size_cls):
        mock_size_json = Mock()
        mock_request_body = Mock()
        mock_request_body.pop.return_value = [mock_size_json]
        result = self.request._extract_sizes(mock_request_body)

        mock_request_body.pop.assert_called_once_with("sizes", [])

        mock_size_cls.from_json.assert_called_once_with(mock_size_json)
        assert result == [mock_size_cls.from_json.return_value]


class TestResizeImageInteractor:
    @classmethod
    def setup_class(cls):
        cls.interactor = ResizeImageInteractor

    def test_init(self):
        mock_resize_image_adapter = Mock()
        mock_request = Mock()

        instance = self.interactor(
            resize_image_adapter=mock_resize_image_adapter,
            request=mock_request,
        )

        assert instance.resize_image_adapter == mock_resize_image_adapter
        assert instance.request == mock_request

    @patcher("ImageEntity")
    def test_run(self, mock_image_entity):
        mock_resized_image_1 = Mock()
        mock_resized_image_2 = Mock()
        mock_image = mock_image_entity.from_json.return_value
        mock_image.resize.side_effect = [
            [mock_resized_image_1, mock_resized_image_2]
        ]
        mock_resize_image_adapter = Mock()
        mock_request = Mock()

        instance = self.interactor(
            resize_image_adapter=mock_resize_image_adapter,
            request=mock_request,
        )

        result = instance.run()

        mock_image_entity.from_json.assert_called_once_with(
            mock_request.request_body
        )

        mock_image.set_resize_adapter.assert_called_once_with(
            mock_resize_image_adapter
        )

        mock_image.resize.assert_called_once_with(mock_request.sizes)

        mock_resized_image_1.to_json.assert_called_once_with()
        mock_resized_image_2.to_json.assert_called_once_with()

        assert result == [
            mock_resized_image_1.to_json.return_value,
            mock_resized_image_2.to_json.return_value,
        ]
