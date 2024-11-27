from typing import Any, Literal

from rest_framework import status
from rest_framework.response import Response

from common.constants import STATUS_CODE_MAPPING, STATUS_MAPPING


def SuccessfulResponse(
    data: Any,
    message: str = "Success!",
    method: Literal["get", "post", "put", "delete"] = "get",
):
    return Response(
        {"msg": message, "data": data},
        status=STATUS_MAPPING.get(method),
    )


def CustomResponse(message: str, status: int):
    return Response({"msg": message}, status=STATUS_CODE_MAPPING.get(status))


def BadResponse(message: str):
    return Response({"msg": message}, status=STATUS_CODE_MAPPING.get(400))
