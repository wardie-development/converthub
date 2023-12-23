from abc import ABC

from chalicelib.basic.basic_converter_adapter import BasicConverterAdapter


class TestBasicConverterAdapter:
    @classmethod
    def setup_class(cls):
        cls.adapter = BasicConverterAdapter

    def test_parent(self):
        assert issubclass(self.adapter, ABC)
