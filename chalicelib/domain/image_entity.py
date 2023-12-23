import base64
from dataclasses import dataclass
from io import BytesIO
from typing import List, Optional

from chalicelib.basic.basic_resize_image_adapter import BasicResizeImageAdapter
from chalicelib.basic.basic_file_entity import BasicFileEntity


@dataclass(frozen=True)
class Size:
    width: int
    height: int

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)

    def to_json(self):
        return {
            "width": self.width,
            "height": self.height,
        }


class ImageEntity(BasicFileEntity):
    def __init__(
        self,
        file_content: str,
        file_type: str,
        file_name: Optional[str] = None,
        size: Optional[Size] = None,
    ):
        self.resize_adapter = None
        self.size = size
        super().__init__(
            file_content=file_content,
            file_type=file_type,
            file_name=file_name,
        )

    def set_resize_adapter(self, resize_adapter: BasicResizeImageAdapter):
        self.resize_adapter = resize_adapter

    def resize(self, sizes: List[Size]) -> List["ImageEntity"]:
        return self.resize_adapter.resize(self, sizes)

    def to_json(self):
        return {
            **super().to_json(),
            "size": self.size.to_json(),
        }

    def get_decoded_file_content(self):
        return BytesIO(base64.b64decode(self.file_content))

    @staticmethod
    def encode_image_bytes(image_bytes):
        return base64.b64encode(image_bytes).decode("utf-8")

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(entity_id={self.entity_id}, "
            f"file_name={self.file_name}, "
            f"file_content={self.file_content[:10]}, "
            f"file_type={self.file_type}, "
            f"size={self.size})"
        )
