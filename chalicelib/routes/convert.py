from chalice import Response

from chalicelib.adapters.getters import ConverterAdapterFactory
from chalicelib.interactors.convert_entity_interactor import (
    ConvertEntityInteractor,
)
from chalicelib.private_blueprint import PrivateBlueprint
from chalicelib.routes.error_codes import get_execution_error

convert_bp = PrivateBlueprint(__name__)


@convert_bp.post("/{convert_from}/{convert_to}")
@get_execution_error(response_cls=Response)
def convert(convert_from, convert_to):
    request_body = convert_bp.body

    converter_adapter = ConverterAdapterFactory.get_adapter(
        file_type_from=convert_from,
        file_type_to=convert_to,
    )

    interactor = ConvertEntityInteractor(
        converter_adapter=converter_adapter, request_body=request_body
    )

    pdf_json = interactor.run()
    file_response_headers = {
        "Content-Type": "application/text",
        "Content-Disposition": f"inline; filename={pdf_json['file_name']}",
        "Content-Transfer-Encoding": "base64",
    }

    return Response(
        headers=file_response_headers,
        body=pdf_json,
    )
