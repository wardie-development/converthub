from unittest.mock import patch, Mock

from chalice import Blueprint

from chalicelib.private_blueprint import PrivateBlueprint


class TestPrivateBlueprint:
    @classmethod
    def setup_class(cls):
        cls.blueprint = PrivateBlueprint

    def test_parent(self):
        assert issubclass(self.blueprint, Blueprint)

    @patch.object(Blueprint, "__init__")
    def test_init(self, mock_super_init):
        mock_name = Mock()
        self.blueprint(mock_name)

        mock_super_init.assert_called_once_with(mock_name)

    @patch.object(PrivateBlueprint, "route")
    @patch("chalicelib.private_blueprint.cors")
    def test_route(self, mock_cors, mock_route):
        mock_name = Mock()
        instance = self.blueprint(mock_name)

        mock_path = Mock()
        mock_method = Mock()

        result = instance._route(mock_path, mock_method)

        mock_route.assert_called_once_with(
            mock_path, methods=[mock_method], cors=mock_cors
        )

        assert result == mock_route.return_value

    @patch.object(PrivateBlueprint, "_route")
    def test_get(self, mock_route):
        mock_name = Mock()
        instance = self.blueprint(mock_name)

        mock_path = Mock()

        result = instance.get(mock_path)

        mock_route.assert_called_once_with(mock_path, "GET")

        assert result == mock_route.return_value

    @patch.object(PrivateBlueprint, "_route")
    def test_post(self, mock_route):
        mock_name = Mock()
        instance = self.blueprint(mock_name)

        mock_path = Mock()

        result = instance.post(mock_path)

        mock_route.assert_called_once_with(mock_path, "POST")

        assert result == mock_route.return_value

    @patch.object(PrivateBlueprint, "_route")
    def test_put(self, mock_route):
        mock_name = Mock()
        instance = self.blueprint(mock_name)

        mock_path = Mock()

        result = instance.put(mock_path)

        mock_route.assert_called_once_with(mock_path, "PUT")

        assert result == mock_route.return_value

    @patch.object(PrivateBlueprint, "_route")
    def test_delete(self, mock_route):
        mock_name = Mock()
        instance = self.blueprint(mock_name)

        mock_path = Mock()

        result = instance.delete(mock_path)

        mock_route.assert_called_once_with(mock_path, "DELETE")

        assert result == mock_route.return_value

    @patch.object(PrivateBlueprint, "current_request")
    def test_body(self, mock_current_request):
        mock_name = Mock()
        instance = self.blueprint(mock_name)

        result = instance.body

        assert result == mock_current_request.json_body
