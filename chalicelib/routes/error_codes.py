from enum import Enum
from typing import Tuple

from chalicelib.adapters.getters import AdapterNotFoundError
from chalicelib.adapters.pillow_txt_to_initials_image_converter_adapter import (
    TxtToInitialsImageConverterError,
)
from chalicelib.adapters.html_to_pdf_adapter import (
    HtmlToPdfConverterError,
)
from chalicelib.adapters.pillow_resize_image_adapter import ResizeImageError


class ErrorAndStatusCode(Enum):
    UNKNOWN_ERROR = 1, 500
    ADAPTER_NOT_FOUND = 2000, 400
    HTML_TO_PDF_CONVERTER_ERROR = 3000, 400
    TXT_TO_WEBP_CONVERTER_ERROR = 3001, 400
    RESIZE_IMAGE_ERROR = 4000, 400


def get_error_and_status_code(error) -> Tuple[int, int]:
    errors = {
        AdapterNotFoundError: ErrorAndStatusCode.ADAPTER_NOT_FOUND,
        HtmlToPdfConverterError: (
            ErrorAndStatusCode.HTML_TO_PDF_CONVERTER_ERROR
        ),
        TxtToInitialsImageConverterError: (
            ErrorAndStatusCode.TXT_TO_WEBP_CONVERTER_ERROR
        ),
        ResizeImageError: ErrorAndStatusCode.RESIZE_IMAGE_ERROR,
    }
    error_code, status_code = errors.get(
        error.__class__, ErrorAndStatusCode.UNKNOWN_ERROR
    ).value
    return error_code, status_code


def get_execution_error(response_cls):
    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_code, status_code = get_error_and_status_code(e)
                return response_cls(
                    status_code=status_code,
                    body={
                        "message": f"{e.__class__.__name__}({e})",
                        "code": error_code,
                    },
                )

        return inner

    return wrapper
