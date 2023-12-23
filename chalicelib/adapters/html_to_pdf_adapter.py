import base64
from io import BytesIO
from time import time

from chalicelib.adapters.providers import BasicHtmlToPdfProvider
from chalicelib.basic.basic_converter_adapter import BasicConverterAdapter
from chalicelib.domain.html_entity import HtmlEntity
from chalicelib.domain.pdf_entity import PdfEntity


class HtmlToPdfConverterError(Exception):
    pass


class HtmlToPdfConverterAdapter(BasicConverterAdapter):
    def __init__(self, provider: BasicHtmlToPdfProvider, logger=None):
        super().__init__(
            entity_cls_from=HtmlEntity, entity_cls_to=PdfEntity, logger=logger
        )
        self.provider = provider

    def convert(self, html: HtmlEntity) -> PdfEntity:
        file_name = html.file_name
        file_type = html.file_type

        try:
            file_content = html.get_decoded_file_content()
            self.logger.info(f"Converting {str(html)} to PDF...")
            start = time()
            pdf = self._make_pdf(file_content, file_name, file_type)
            end = time()
            self.logger.info(
                f"Successfully converted {str(html)} " f"to PDF ({str(pdf)})"
            )
            self.logger.info(f"Conversion took {end - start} seconds")
            return pdf
        except Exception as e:
            message = (
                f"Error converting {file_name} "
                f"to PDF: {e.__class__.__name__}({e})"
            )
            self.logger.error(message)
            raise HtmlToPdfConverterError(message)

    def _make_pdf(self, file_content, file_name, file_type):
        pdf_bytes = self._make_pdf_bytes(file_content)
        pdf = PdfEntity(
            file_name=file_name.replace(file_type, "pdf"),
            file_content=base64.b64encode(pdf_bytes.getvalue()).decode(
                "utf-8"
            ),
        )
        return pdf

    def _make_pdf_bytes(self, file_content: str) -> BytesIO:
        return self.provider.make_pdf_bytes(file_content)
