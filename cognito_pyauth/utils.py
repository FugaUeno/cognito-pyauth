from fastapi import Security
from fastapi.security import APIKeyHeader
from fastapi.security.utils import get_authorization_scheme_param

api_key = APIKeyHeader(name="Authorization")


def get_api_token(authorization: str = Security(api_key)) -> str:
    _, token = get_authorization_scheme_param(authorization)
    return token
