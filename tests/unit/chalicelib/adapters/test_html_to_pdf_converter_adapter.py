from unittest.mock import patch, Mock, call, MagicMock

import pytest

from chalicelib.adapters.getters import HtmlToPdfConverterAdapter
from chalicelib.adapters.html_to_pdf_adapter import (
    HtmlToPdfConverterError,
)
from chalicelib.basic.basic_converter_adapter import BasicConverterAdapter
from chalicelib.domain.html_entity import HtmlEntity
from chalicelib.domain.pdf_entity import PdfEntity


def patcher(obj):
    prefix = "chalicelib.adapters.html_to_pdf_adapter"

    return patch(f"{prefix}.{obj}")


class TestHtmlToPdfConverterAdapter:
    @patch.object(BasicConverterAdapter, "__init__")
    def make_sut(self, mock_super_init):
        mock_logger = Mock()
        mock_provider = Mock()

        sut = self.adapter(mock_provider, mock_logger)

        mock_super_init.assert_called_once_with(
            entity_cls_from=HtmlEntity,
            entity_cls_to=PdfEntity,
            logger=mock_logger,
        )

        assert sut.provider == mock_provider
        sut.logger = mock_logger
        return sut

    @classmethod
    def setup_class(cls):
        cls.adapter = HtmlToPdfConverterAdapter

    def test_parent(self):
        assert issubclass(self.adapter, BasicConverterAdapter)

    @patcher("time")
    @patch.object(HtmlToPdfConverterAdapter, "_make_pdf")
    def test_convert_successfully(self, mock_make_pdf, mock_time):
        mock_html = Mock()

        sut = self.make_sut()

        mock_start = MagicMock()
        mock_end = MagicMock()

        mock_time.side_effect = [mock_start, mock_end]

        result = sut.convert(mock_html)

        mock_html.get_decoded_file_content.assert_called_once_with()

        sut.logger.info.assert_has_calls(
            [
                call(f"Converting {str(mock_html)} to PDF..."),
                call(
                    f"Successfully converted {str(mock_html)} "
                    f"to PDF ({str(mock_make_pdf.return_value)})"
                ),
                call(
                    f"Conversion took {mock_end.__sub__.return_value} "
                    "seconds"
                ),
            ]
        )

        mock_end.__sub__.assert_called_once_with(mock_start)

        mock_make_pdf.assert_called_once_with(
            mock_html.get_decoded_file_content.return_value,
            mock_html.file_name,
            mock_html.file_type,
        )

        assert result == mock_make_pdf.return_value

    @patcher("time")
    @patch.object(HtmlToPdfConverterAdapter, "_make_pdf")
    def test_convert_raising_error(self, mock_make_pdf, _mock_time):
        error = Exception("error")
        mock_make_pdf.side_effect = error
        mock_html = Mock()

        sut = self.make_sut()

        with pytest.raises(HtmlToPdfConverterError) as error:
            sut.convert(mock_html)

        error_message = (
            f"Error converting {mock_html.file_name} "
            "to PDF: Exception(error)"
        )

        sut.logger.error.assert_called_once_with(error_message)

        assert str(error.value) == error_message

    @patcher("PdfEntity")
    @patcher("base64.b64encode")
    @patch.object(HtmlToPdfConverterAdapter, "_make_pdf_bytes")
    def test_make_pdf(self, mock_make_pdf_bytes, mock_b64encode, mock_pdf):
        mock_file_content = Mock()
        mock_file_name = Mock()
        mock_file_type = Mock()
        mock_provider = Mock()

        instance = self.adapter(mock_provider)

        result = instance._make_pdf(
            mock_file_content, mock_file_name, mock_file_type
        )

        mock_make_pdf_bytes.assert_called_once_with(mock_file_content)
        mock_make_pdf_bytes.return_value.getvalue.assert_called_once_with()
        mock_b64encode.assert_called_once_with(
            mock_make_pdf_bytes.return_value.getvalue.return_value
        )
        mock_file_name.replace.assert_called_once_with(mock_file_type, "pdf")
        mock_b64encode.return_value.decode.assert_called_once_with("utf-8")
        mock_pdf.assert_called_once_with(
            file_name=mock_file_name.replace.return_value,
            file_content=mock_b64encode.return_value.decode.return_value,
        )

        assert result == mock_pdf.return_value

    def test_make_pdf_bytes(self):
        mock_file_content = Mock()

        sut = self.make_sut()

        result = sut._make_pdf_bytes(mock_file_content)

        sut.provider.make_pdf_bytes.assert_called_once_with(mock_file_content)

        assert result == sut.provider.make_pdf_bytes.return_value
