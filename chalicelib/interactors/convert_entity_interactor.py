from typing import Dict

from chalicelib.basic.basic_converter_adapter import BasicConverterAdapter


class ConvertEntityInteractor:
    def __init__(
        self,
        converter_adapter: BasicConverterAdapter,
        request_body: Dict,
    ):
        self.converter_adapter = converter_adapter
        self.request_body = request_body

    def run(self) -> Dict:
        entity = self.converter_adapter.entity_cls_from.from_json(
            self.request_body
        )
        entity.set_converter_adapter(self.converter_adapter)
        converted_entity = entity.convert()

        return converted_entity.to_json()
