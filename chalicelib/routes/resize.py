from chalice import Response

from chalicelib.adapters.getters import get_pillow_resize_image_adapter
from chalicelib.interactors.resize_image_interactor import (
    ResizeImageRequest,
    ResizeImageInteractor,
)
from chalicelib.private_blueprint import PrivateBlueprint
from chalicelib.routes.error_codes import get_execution_error

resize_bp = PrivateBlueprint(__name__)


@resize_bp.post("/")
@get_execution_error(response_cls=Response)
def resize():
    body = resize_bp.body
    request = ResizeImageRequest(body)
    resize_image_adapter = get_pillow_resize_image_adapter()
    interactor = ResizeImageInteractor(
        resize_image_adapter=resize_image_adapter,
        request=request,
    )
    resized_images_json = interactor.run()

    return Response(body={"resized_images": resized_images_json})
