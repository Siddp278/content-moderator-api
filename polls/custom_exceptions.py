# Custom exception

from rest_framework.exceptions import APIException

class CatalogExeption(APIException):
    status_code = 503
    default_detail = 'Unable to create catalog'
    default_code = '4026'