from typing import List

import jwt
import requests
from pydantic import BaseModel


class Key(BaseModel):
    alg: str
    e: str
    kid: str
    kty: str
    n: str
    use: str


class Config:
    region: str
    pool_id: str
    client_id: str
    cognito_url: str
    cognito_jwk_url: str
    public_keys: List[Key] = []

    def __init__(
        self,
        *,
        region: str,
        pool_id: str,
        client_id: str,
    ) -> None:
        self.region = region
        self.pool_id = pool_id
        self.client_id = client_id

        url_format = "https://cognito-idp.{}.amazonaws.com/{}"
        self.cognito_url = url_format.format(
            self.region,
            self.pool_id,
        )
        self.cognito_jwk_url = f"{self.cognito_url}/.well-known/jwks.json"

        self._init_public_keys()

    def get_public_key(self, kid: str) -> str:
        for key in self.public_keys:
            if key.kid == kid:
                return jwt.algorithms.RSAAlgorithm.from_jwk(key.json())
        else:
            raise Exception("not found public key")

    def _init_public_keys(self) -> None:
        res = requests.get(self.cognito_jwk_url)
        for key in res.json()["keys"]:
            self.public_keys.append(Key(**key))
