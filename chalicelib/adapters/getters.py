import logging
from dataclasses import dataclass

from chalicelib.adapters.pillow_txt_to_initials_image_converter_adapter import (
    PillowTxtToInitialsImageConverterAdapter,
)
from chalicelib.adapters.pillow_resize_image_adapter import (
    PillowResizeImageAdapter,
)
from chalicelib.adapters.html_to_pdf_adapter import HtmlToPdfConverterAdapter
from chalicelib.adapters.providers import PdfKitHtmlToPdfProvider
from chalicelib.domain.image_entity import ImageEntity

logger = logging.getLogger(__name__)


def get_html_to_pdf_converter_adapter():
    provider = PdfKitHtmlToPdfProvider()
    return HtmlToPdfConverterAdapter(provider=provider, logger=logger)


def get_txt_to_webp_converter_adapter():
    return PillowTxtToInitialsImageConverterAdapter(
        logger=logger, file_type_to="webp"
    )


def get_pillow_resize_image_adapter():
    return PillowResizeImageAdapter(logger=logger, image_cls=ImageEntity)


class AdapterNotFoundError(NotImplementedError):
    pass


@dataclass(frozen=True)
class ConverterKey:
    file_type_from: str
    file_type_to: str
    DELIMITER = "->"

    def __str__(self):
        return f"{self.file_type_from}{self.DELIMITER}{self.file_type_to}"


class ConverterAdapterFactory:
    """
    Factory for getting the correct adapter for a given conversion.
    Every time a new adapter is added, it must be added to the ADAPTERS,
    with the key being the ConverterKey.
    """

    ADAPTERS = {
        ConverterKey("html", "pdf"): get_html_to_pdf_converter_adapter,
        ConverterKey("txt", "webp"): get_txt_to_webp_converter_adapter,
    }

    @classmethod
    def get_adapter(cls, file_type_from, file_type_to):
        converter_key = ConverterKey(file_type_from, file_type_to)
        adapter = cls.ADAPTERS.get(converter_key)

        if adapter is None:
            raise AdapterNotFoundError(
                f"Adapter not found for {converter_key}"
            )

        return adapter()
