from abc import ABC

from chalicelib.basic.basic_resize_image_adapter import BasicResizeImageAdapter


class TestBasicResizeImageAdapter:
    @classmethod
    def setup_class(cls):
        cls.adapter = BasicResizeImageAdapter

    def test_parent(self):
        assert issubclass(self.adapter, ABC)
