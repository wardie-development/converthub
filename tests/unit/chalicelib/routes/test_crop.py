from unittest.mock import patch

from chalicelib.routes.resize import resize


def patcher(obj):
    prefix = "chalicelib.routes.resize"

    return patch(f"{prefix}.{obj}")


@patcher("resize_bp")
@patcher("ResizeImageRequest")
@patcher("ResizeImageInteractor")
@patcher("get_pillow_resize_image_adapter")
@patcher("Response")
def test_resize(
    mock_response,
    mock_get_pillow_resize_image_adapter,
    mock_resize_image_interactor,
    mock_resize_image_request,
    mock_resize_bp,
):
    response = resize()

    mock_resize_image_request.assert_called_once_with(mock_resize_bp.body)
    mock_request = mock_resize_image_request.return_value

    mock_get_pillow_resize_image_adapter.assert_called_once_with()

    mock_resize_image_interactor.assert_called_once_with(
        resize_image_adapter=mock_get_pillow_resize_image_adapter.return_value,
        request=mock_request,
    )
    mock_interactor = mock_resize_image_interactor.return_value
    mock_interactor.run.assert_called_once_with()
    mock_interactor_response = mock_interactor.run.return_value

    mock_response.assert_called_once_with(
        body={"resized_images": mock_interactor_response}
    )

    assert response == mock_response.return_value
