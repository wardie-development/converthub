import base64
from typing import Optional, Dict
from uuid import uuid4

from chalicelib.basic.basic_converter_adapter import BasicConverterAdapter


class BasicFileEntity:
    def __init__(
        self,
        file_content: str,
        file_type: str,
        file_name: Optional[str] = None,
        entity_id: Optional[str] = None,
    ):
        self.converter_adapter = None
        self.entity_id = entity_id or str(uuid4())

        self.file_name = file_name or f"{self.entity_id}.{file_type}"
        self.file_content = file_content
        self.file_type = file_type

    def set_converter_adapter(self, converter_adapter: BasicConverterAdapter):
        self.converter_adapter = converter_adapter

    def convert(self) -> "BasicFileEntity":
        return self.converter_adapter.convert(self)

    @classmethod
    def from_json(cls, json_data: Dict):
        return cls(**json_data)

    def to_json(self):
        return {
            "file_name": self.file_name,
            "file_content": self.file_content,
            "file_type": self.file_type,
            "entity_id": self.entity_id,
        }

    def get_decoded_file_content(self):
        return base64.b64decode(self.file_content).decode("utf-8")

    def __eq__(self, other: "BasicFileEntity"):
        return self.entity_id == other.entity_id

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(entity_id={self.entity_id}, "
            f"file_name={self.file_name}, "
            f"file_content={self.file_content[:10]}, "
            f"file_type={self.file_type})"
        )

    def __str__(self):
        return self.__repr__()
