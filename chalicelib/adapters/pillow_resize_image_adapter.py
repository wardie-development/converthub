from io import BytesIO
from typing import List, Type
from PIL import Image
from time import time

from chalicelib.basic.basic_resize_image_adapter import BasicResizeImageAdapter
from chalicelib.domain.image_entity import ImageEntity, Size


class ResizeImageError(Exception):
    pass


class PillowResizeImageAdapter(BasicResizeImageAdapter):
    def __init__(self, image_cls: Type[ImageEntity], logger=None):
        super().__init__(image_cls=image_cls, logger=logger)

    def resize(
        self, entity_to_resize: ImageEntity, sizes: List[Size]
    ) -> List[ImageEntity]:
        self.logger.info(f"Resizing image {entity_to_resize}")
        start = time()
        resized_images = self._resize_images(entity_to_resize, sizes)
        end = time()
        self.logger.info("Resized images successfully")
        self.logger.info(f"Resize took {end - start} seconds")
        return resized_images

    def _resize_images(
        self, entity_to_resize: ImageEntity, sizes: List[Size]
    ) -> List[ImageEntity]:
        sizes_without_duplicates = list(set(sizes))
        resized_images = []

        for size in sizes_without_duplicates:
            resized_image = self._resize_image(entity_to_resize, size)
            resized_images.append(resized_image)
            self.logger.info(f"Resized image {resized_image}")

        return resized_images

    def _resize_image(self, image: ImageEntity, size: Size) -> ImageEntity:
        try:
            image_content = image.get_decoded_file_content()
            opened_image = Image.open(image_content)

            resized_image = opened_image.resize((size.width, size.height))
            image_bytes = BytesIO()
            resized_image.save(image_bytes, format=opened_image.format)

            image_content = self.image_cls.encode_image_bytes(
                image_bytes.getvalue()
            )

            return self.image_cls(
                file_content=image_content,
                file_type=opened_image.format.lower(),
                file_name=f"{size.width}x{size.height}_{image.file_name}",
                size=size,
            )
        except Exception as e:
            message = (
                f"Error resizing image {image}: "
                f"{e.__class__.__name__}({e})"
            )
            self.logger.error(message)
            raise ResizeImageError(message)
