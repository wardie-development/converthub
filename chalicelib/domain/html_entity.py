from typing import Optional

from chalicelib.basic.basic_file_entity import BasicFileEntity


class HtmlEntity(BasicFileEntity):
    def __init__(
        self,
        file_content: str,
        file_name: Optional[str] = None,
        entity_id: Optional[str] = None,
    ):
        super().__init__(
            file_content=file_content,
            file_name=file_name,
            file_type="html",
            entity_id=entity_id,
        )
