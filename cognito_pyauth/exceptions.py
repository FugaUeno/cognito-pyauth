from fastapi import HTTPException, status


class UserNotConfirmedException(Exception):
    pass


class NotAuthorizedException(Exception):
    pass


class UsernameExistsException(Exception):
    pass


NotAuthorizedHTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="un authorized",
    headers={"WWW-Authenticate": "Bearer"},
)
