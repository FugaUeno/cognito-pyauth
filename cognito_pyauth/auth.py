from typing import Any, Dict

import boto3
import jwt
from fastapi import Depends

from cognito_pyauth import exceptions, schemas
from cognito_pyauth.config import Config
from cognito_pyauth.utils import get_api_token


class Auth:
    config: Config
    client: Any

    def __init__(self, config: Config) -> None:
        self.config = config
        self.client = boto3.client(
            "cognito-idp",
            region_name=self.config.region,
        )

    def get_payload(
        self,
        token: str = Depends(get_api_token),
    ) -> schemas.Payload:
        try:
            jwt_header = jwt.get_unverified_header(token)
            jwt_algorithms = jwt_header["alg"]
            public_key = self.config.get_public_key(jwt_header["kid"])
            decoded = jwt.decode(
                token,
                public_key,
                algorithms=[jwt_algorithms],
                verify=True,
                options={"require_exp": True},
                audience=self.config.client_id,
            )
            return schemas.Payload(
                **decoded,
                username=decoded["cognito:username"],
            )
        except Exception:
            raise exceptions.NotAuthorizedException()

    def get_payload_depends(
        self,
        token: str = Depends(get_api_token),
    ) -> schemas.Payload:
        try:
            return self.get_payload(token)
        except exceptions.NotAuthorizedException:
            raise exceptions.NotAuthorizedHTTPException

    def login(
        self,
        username: str,
        password: str,
    ) -> schemas.AuthenticationResult:
        req = schemas.LoginRequest(
            username=username,
            password=password,
        )

        try:
            res = self.client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": req.username,
                    "PASSWORD": req.password.get_secret_value(),
                },
                ClientId=self.config.client_id,
            )
        except self.client.exceptions.UserNotConfirmedException as e:
            raise exceptions.UserNotConfirmedException(e)
        except self.client.exceptions.NotAuthorizedException as e:
            raise exceptions.NotAuthorizedException(e)

        result = res["AuthenticationResult"]
        return schemas.AuthenticationResult(
            access_token=result["AccessToken"],
            id_token=result["IdToken"],
            refresh_token=result["RefreshToken"],
            token_type=result["TokenType"],
            expires_in=result["ExpiresIn"],
        )

    def signup(
        self,
        username: str,
        password: str,
    ) -> Dict[str, Any]:
        req = schemas.SignupRequest(
            username=username,
            password=password,
        )

        try:
            return self.client.sign_up(
                Username=req.username,
                Password=req.password.get_secret_value(),
                ClientId=self.config.client_id,
            )
        except self.client.exceptions.UsernameExistsException as e:
            raise exceptions.UsernameExistsException(e)

    def confirm_signup(
        self,
        username: str,
        confirmation_code: str,
    ) -> Dict[str, Any]:
        req = schemas.ConfirmSignupRequest(
            username=username,
            confirmation_code=confirmation_code,
        )
        return self.client.confirm_sign_up(
            Username=req.username,
            ConfirmationCode=req.confirmation_code,
            ClientId=self.config.client_id,
        )

    def resend_confirmation_code(
        self,
        username: str,
    ) -> Dict[str, Any]:
        req = schemas.ResendConfirmationCodeRequest(
            username=username,
        )
        return self.client.resend_confirmation_code(
            Username=req.username,
            ClientId=self.config.client_id,
        )

    def delete_user(
        self,
        username: str,
        password: str,
    ) -> Dict[str, Any]:
        res = self.login(username, password)
        return self.client.delete_user(
            AccessToken=res.access_token,
        )

    def delete_user_by_access_token(
        self,
        access_token: str,
    ) -> Dict[str, Any]:
        return self.client.delete_user(
            AccessToken=access_token,
        )

    def refresh_token(
        self,
        refresh_token: str,
    ) -> schemas.RefreshTokenResult:
        req = schemas.TokenRefreshRequest(refresh_token=refresh_token)

        res = self.client.initiate_auth(
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": req.refresh_token,
            },
            ClientId=self.config.client_id,
        )
        result = res["AuthenticationResult"]
        return schemas.RefreshTokenResult(
            access_token=result["AccessToken"],
            id_token=result["IdToken"],
            token_type=result["TokenType"],
            expires_in=result["ExpiresIn"],
        )
