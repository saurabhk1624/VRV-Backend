from rest_framework import status

STATUS_MAPPING = {
    "get": status.HTTP_200_OK,
    "post": status.HTTP_201_CREATED,
    "put": status.HTTP_202_ACCEPTED,
    "delete": status.HTTP_204_NO_CONTENT,
}

STATUS_CODE_MAPPING = {
    200: status.HTTP_200_OK,
    201: status.HTTP_201_CREATED,
    202: status.HTTP_202_ACCEPTED,
    400: status.HTTP_400_BAD_REQUEST,
    401: status.HTTP_401_UNAUTHORIZED,
    403: status.HTTP_403_FORBIDDEN,
    405: status.HTTP_405_METHOD_NOT_ALLOWED,
}
