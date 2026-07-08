from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Envuelve las respuestas de error de DRF en un sobre JSON consistente.

    Formato: {"error": {"status_code": <int>, "detail": <payload original>}}
    Mantiene el status HTTP y el detalle original de DRF; solo unifica la forma.
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'error': {
                'status_code': response.status_code,
                'detail': response.data,
            }
        }

    return response
