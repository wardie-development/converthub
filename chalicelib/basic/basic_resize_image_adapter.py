from abc import ABC, abstractmethod
from typing import List


class BasicResizeImageAdapter(ABC):
    def __init__(self, image_cls, logger=None):
        self.image_cls = image_cls  # pragma: no cover
        self.logger = logger  # pragma: no cover

    @abstractmethod
    def resize(self, entity_to_resize, sizes: List):
        raise NotImplementedError  # pragma: no cover
