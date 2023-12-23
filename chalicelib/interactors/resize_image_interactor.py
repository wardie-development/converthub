from typing import Dict, List

from chalicelib.adapters.pillow_resize_image_adapter import (
    PillowResizeImageAdapter,
)
from chalicelib.domain.image_entity import ImageEntity, Size


class ResizeImageRequest:
    def __init__(self, request_body: Dict):
        self.sizes = self._extract_sizes(request_body)
        self.request_body = request_body

    @staticmethod
    def _extract_sizes(request_body) -> List[Size]:
        request_sizes = request_body.pop("sizes", [])
        return [Size.from_json(size) for size in request_sizes]


class ResizeImageInteractor:
    def __init__(
        self,
        resize_image_adapter: PillowResizeImageAdapter,
        request: ResizeImageRequest,
    ):
        self.resize_image_adapter = resize_image_adapter
        self.request = request

    def run(self):
        image = ImageEntity.from_json(self.request.request_body)
        image.set_resize_adapter(self.resize_image_adapter)
        resized_images: List[ImageEntity] = image.resize(self.request.sizes)
        return [resized_image.to_json() for resized_image in resized_images]
