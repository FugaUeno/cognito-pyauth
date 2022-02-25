from dotenv import load_dotenv
from fastapi import Depends, FastAPI, status
from fastapi.testclient import TestClient

from cognito_pyauth import Auth
from cognito_pyauth.schemas import Payload
from tests.testutil import logger  # noqa: F401
from tests.testutil import config, token

load_dotenv(".env.test")

app = FastAPI()


auth = Auth(config)


@app.get("/foo")
def foo(payload: Payload = Depends(auth.get_payload_depends)) -> str:
    return "foo"


client = TestClient(app)


def test_valid_auth() -> None:
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/foo", headers=headers)
    assert res.status_code == status.HTTP_200_OK


def test_invalid_auth() -> None:
    headers = {"Authorization": f"Bearer {token}-test"}
    res = client.get("/foo", headers=headers)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
