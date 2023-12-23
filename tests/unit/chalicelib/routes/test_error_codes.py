from unittest.mock import Mock, patch

from chalicelib.routes.error_codes import (
    ErrorAndStatusCode,
    get_execution_error,
    get_error_and_status_code,
)


def patcher(obj):
    prefix = "chalicelib.routes.error_codes"

    return patch(f"{prefix}.{obj}")


class TestErrorAndStatusCode:
    @classmethod
    def setup_class(cls):
        cls.enum = ErrorAndStatusCode

    def test_enum(self):
        assert self.enum.UNKNOWN_ERROR.value == (1, 500)
        assert self.enum.ADAPTER_NOT_FOUND.value == (2000, 400)
        assert self.enum.HTML_TO_PDF_CONVERTER_ERROR.value == (3000, 400)
        assert self.enum.RESIZE_IMAGE_ERROR.value == (4000, 400)


def test_get_error_and_status_code():
    mock_error = Mock()

    result = get_error_and_status_code(mock_error)

    assert result == ErrorAndStatusCode.UNKNOWN_ERROR.value


@patcher("get_error_and_status_code")
def test_get_execution_error_without_error(mock_get_error_and_status_code):
    mock_response_cls = Mock()
    mock_func = Mock()
    mock_args = ["some", "args"]
    mock_kwargs = {"some": "kwargs"}

    wrapper = get_execution_error(mock_response_cls)
    inner = wrapper(mock_func)

    result = inner(*mock_args, **mock_kwargs)

    mock_func.assert_called_once_with(*mock_args, **mock_kwargs)

    mock_get_error_and_status_code.assert_not_called()
    mock_response_cls.assert_not_called()

    assert result == mock_func.return_value


@patcher("get_error_and_status_code")
def test_get_execution_error_with_error(mock_get_error_and_status_code):
    mock_error_code = Mock()
    mock_status_code = Mock()
    mock_get_error_and_status_code.return_value = (
        mock_error_code,
        mock_status_code,
    )
    error = Exception("some error")
    mock_response_cls = Mock()
    mock_func = Mock(side_effect=error)
    mock_args = ["some", "args"]
    mock_kwargs = {"some": "kwargs"}

    wrapper = get_execution_error(mock_response_cls)
    inner = wrapper(mock_func)

    result = inner(*mock_args, **mock_kwargs)

    mock_func.assert_called_once_with(*mock_args, **mock_kwargs)

    mock_get_error_and_status_code.assert_called_once_with(error)
    mock_response_cls.assert_called_once_with(
        status_code=mock_status_code,
        body={
            "message": "Exception(some error)",
            "code": mock_error_code,
        },
    )

    assert result == mock_response_cls.return_value
