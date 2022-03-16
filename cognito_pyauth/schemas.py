from pydantic import BaseModel, Field, SecretStr, validator


class Payload(BaseModel):
    sub: str
    email_verified: bool
    iss: str
    username: str
    origin_jti: str
    aud: str
    event_id: str
    token_use: str
    auth_time: str
    exp: str
    iat: str
    jti: str
    email: str


class AuthenticationResult(BaseModel):
    access_token: str = Field(title="アクセストークン")
    id_token: str = Field(title="IDトークン")
    refresh_token: str = Field(title="更新トークン")
    token_type: str = Field(title="トークンタイプ")
    expires_in: int = Field(title="トークンが有効な秒数")


class RefreshTokenResult(BaseModel):
    access_token: str = Field(title="アクセストークン")
    id_token: str = Field(title="IDトークン")
    token_type: str = Field(title="トークンタイプ")
    expires_in: int = Field(title="トークンが有効な秒数")


class SignupRequest(BaseModel):
    username: str = Field(title="ユーザー名")
    password: SecretStr = Field(title="パスワード", min_length=4)


class LoginRequest(BaseModel):
    username: str = Field(title="ユーザー名")
    password: SecretStr = Field(title="パスワード", min_length=4)


class ConfirmSignupRequest(BaseModel):
    username: str = Field(title="ユーザー名")
    confirmation_code: str = Field(title="検証コード", min_length=6, max_length=6)

    @validator("confirmation_code")
    def confirmation_code_validator(cls, v: str) -> str:
        if not v.isnumeric():
            raise ValueError("検証コードは6桁の数字です")
        return v


class ResendConfirmationCodeRequest(BaseModel):
    username: str = Field(title="ユーザー名")


class TokenRefreshRequest(BaseModel):
    refresh_token: str = Field(title="更新トークン")
