from unittest.mock import Mock, patch

from chalicelib.routes.convert import convert


def patcher(obj):
    prefix = "chalicelib.routes.convert"

    return patch(f"{prefix}.{obj}")


@patcher("convert_bp")
@patcher("ConverterAdapterFactory")
@patcher("ConvertEntityInteractor")
@patcher("Response")
def test_convert(
    mock_response,
    mock_convert_entity_interactor,
    mock_adapter_factory,
    mock_convert_bp,
):
    mock_convert_from = Mock()
    mock_convert_to = Mock()

    response = convert(mock_convert_from, mock_convert_to)

    mock_adapter_factory.get_adapter.assert_called_once_with(
        file_type_from=mock_convert_from,
        file_type_to=mock_convert_to,
    )
    mock_converter_adapter = mock_adapter_factory.get_adapter.return_value

    mock_convert_entity_interactor.assert_called_once_with(
        converter_adapter=mock_converter_adapter,
        request_body=mock_convert_bp.body,
    )
    mock_interactor = mock_convert_entity_interactor.return_value
    mock_interactor.run.assert_called_once_with()
    mock_interactor_response = mock_interactor.run.return_value
    mock_interactor_response.__getitem__.assert_called_once_with("file_name")

    mock_response.assert_called_once_with(
        headers={
            "Content-Type": "application/text",
            "Content-Disposition": (
                "inline; filename="
                f"{mock_interactor_response.__getitem__.return_value}"
            ),
            "Content-Transfer-Encoding": "base64",
        },
        body=mock_interactor_response,
    )

    assert response == mock_response.return_value
