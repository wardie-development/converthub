from unittest.mock import patch, Mock

import pytest

from chalicelib.adapters.getters import (
    get_html_to_pdf_converter_adapter,
    get_pillow_resize_image_adapter,
    ConverterKey,
    ConverterAdapterFactory,
    AdapterNotFoundError,
    get_txt_to_webp_converter_adapter,
)


def patcher(obj):
    prefix = "chalicelib.adapters.getters"

    return patch(f"{prefix}.{obj}")


@patcher("HtmlToPdfConverterAdapter")
@patcher("PdfKitHtmlToPdfProvider")
@patcher("logger")
def test_get_html_to_pdf_converter_adapter(
    mock_logger, mock_pdf_kit_html_to_pdf_provider, mock_html_to_pdf_adapter
):
    result = get_html_to_pdf_converter_adapter()

    mock_pdf_kit_html_to_pdf_provider.assert_called_once_with()
    mock_provider = mock_pdf_kit_html_to_pdf_provider.return_value
    mock_html_to_pdf_adapter.assert_called_once_with(
        provider=mock_provider, logger=mock_logger
    )

    assert result == mock_html_to_pdf_adapter.return_value


@patcher("PillowTxtToInitialsImageConverterAdapter")
@patcher("logger")
def test_get_txt_to_webp_converter_adapter(
    mock_logger, mock_pillow_txt_to_initials_image_converter_adapter
):
    result = get_txt_to_webp_converter_adapter()

    (
        mock_pillow_txt_to_initials_image_converter_adapter.assert_called_once_with(
            logger=mock_logger, file_type_to="webp"
        )
    )

    assert result == (
        mock_pillow_txt_to_initials_image_converter_adapter.return_value
    )


@patcher("PillowResizeImageAdapter")
@patcher("ImageEntity")
@patcher("logger")
def test_get_pillow_resize_image_adapter(
    mock_logger, mock_image_entity, mock_pillow_resize_image_adapter
):
    result = get_pillow_resize_image_adapter()

    mock_pillow_resize_image_adapter.assert_called_once_with(
        logger=mock_logger, image_cls=mock_image_entity
    )

    assert result == mock_pillow_resize_image_adapter.return_value


class TestConverterKey:
    @classmethod
    def setup_class(cls):
        cls.key = ConverterKey

    def test_delimiter(self):
        assert self.key.DELIMITER == "->"

    def test_str(self):
        mock_file_type_from = Mock()
        mock_file_type_to = Mock()

        key = self.key(
            file_type_from=mock_file_type_from,
            file_type_to=mock_file_type_to,
        )

        result = str(key)

        assert result == (
            f"{mock_file_type_from}{self.key.DELIMITER}{mock_file_type_to}"
        )


class TestConverterAdapterFactory:
    @classmethod
    def setup_class(cls):
        cls.factory = ConverterAdapterFactory

    def test_adapters(self):
        assert self.factory.ADAPTERS == {
            ConverterKey("html", "pdf"): get_html_to_pdf_converter_adapter,
            ConverterKey("txt", "webp"): get_txt_to_webp_converter_adapter,
        }

    @patcher("HtmlToPdfConverterAdapter")
    def test_get_adapter_successfully(
        self, mock_html_to_pdf_converter_adapter
    ):
        mock_file_type_from = "html"
        mock_file_type_to = "pdf"

        result = self.factory.get_adapter(
            mock_file_type_from, mock_file_type_to
        )

        assert result == mock_html_to_pdf_converter_adapter.return_value

    def test_get_adapter_raising_error(self):
        mock_file_type_from = Mock()
        mock_file_type_to = Mock()

        with pytest.raises(AdapterNotFoundError) as error:
            self.factory.get_adapter(mock_file_type_from, mock_file_type_to)

        assert str(error.value) == (
            f"Adapter not found for "
            f"{ConverterKey(mock_file_type_from, mock_file_type_to)}"
        )
