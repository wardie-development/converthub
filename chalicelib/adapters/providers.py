from abc import abstractmethod, ABC
from io import BytesIO

import pdfkit


class BasicHtmlToPdfProvider(ABC):
    @staticmethod
    @abstractmethod
    def make_pdf_bytes(file_content: str) -> BytesIO:
        """
        :param file_content: File content as plain text, not encoded
        :return: BytesIO object with the PDF content
        """
        raise NotImplementedError  # pragma: no cover


class PdfKitHtmlToPdfProvider(BasicHtmlToPdfProvider):
    @staticmethod
    def make_pdf_bytes(file_content: str) -> BytesIO:
        convert_config = pdfkit.configuration(
            wkhtmltopdf="/opt/bin/wkhtmltopdf"
        )
        options = {
            'page-size': 'A4',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
        }

        pdf_bytes = pdfkit.from_string(
            input=file_content,
            output_path=False,
            configuration=convert_config,
            options=options,
        )

        return BytesIO(pdf_bytes)
