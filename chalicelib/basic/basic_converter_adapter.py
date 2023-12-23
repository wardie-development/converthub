from abc import ABC, abstractmethod


class BasicConverterAdapter(ABC):
    def __init__(self, entity_cls_from, entity_cls_to, logger=None):
        self.entity_cls_from = entity_cls_from
        self.entity_cls_to = entity_cls_to
        self.logger = logger  # pragma: no cover

    @abstractmethod
    def convert(self, entity_to_convert):
        raise NotImplementedError  # pragma: no cover
