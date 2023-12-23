from unittest.mock import patch, Mock

from chalicelib.adapters.providers import (
    BasicHtmlToPdfProvider,
    PdfKitHtmlToPdfProvider,
)


def patcher(obj):
    prefix = "chalicelib.adapters.providers"

    return patch(f"{prefix}.{obj}")


class TestPdfKitHtmlToPdfProvider:
    @classmethod
    def setup_class(cls):
        cls.provider = PdfKitHtmlToPdfProvider

    def test_parent(self):
        assert issubclass(self.provider, BasicHtmlToPdfProvider)

    @patcher("BytesIO")
    @patcher("pdfkit")
    def test_make_pdf_bytes(self, mock_pdfkit, mock_bytes_io):
        mock_file_content = Mock()

        sut = self.provider()

        result = sut.make_pdf_bytes(mock_file_content)

        # Not use called_once_>with< because use a wkhtmltopdf path.
        mock_pdfkit.configuration.assert_called_once()

        mock_config = mock_pdfkit.configuration.return_value

        mock_pdfkit.from_string.assert_called_once_with(
            input=mock_file_content,
            output_path=False,
            configuration=mock_config,
            options={
                "page-size": "A4",
                "margin-top": "0mm",
                "margin-right": "0mm",
                "margin-bottom": "0mm",
                "margin-left": "0mm",
            },
        )
        mock_bytes_io.assert_called_once_with(
            mock_pdfkit.from_string.return_value
        )
        mock_bytes = mock_bytes_io.return_value

        assert result == mock_bytes
