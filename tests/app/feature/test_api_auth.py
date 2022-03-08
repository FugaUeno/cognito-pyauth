from dotenv import load_dotenv
from fastapi import Depends, FastAPI, status
from fastapi.testclient import TestClient

from cognito_pyauth import Auth
from cognito_pyauth.schemas import Payload
from tests.testutil import logger  # noqa: F401
from tests.testutil import config

load_dotenv(".env.test")

app = FastAPI()


auth = Auth(config)


@app.get("/foo")
def foo(payload: Payload = Depends(auth.get_payload_depends)) -> str:
    return "foo"


client = TestClient(app)

test_username = input("メールアドレス:")
test_password = "Test_1234"
id_token = ""


def test_signup() -> None:
    auth.signup(test_username, test_password)


def test_confirm_signup() -> None:
    confirmation_code = input("検証コード:")
    auth.confirm_signup(test_username, confirmation_code)


def test_login() -> None:
    global id_token
    res = auth.login(test_username, test_password)
    id_token = res.id_token


def test_valid_auth() -> None:
    headers = {"Authorization": f"Bearer {id_token}"}
    res = client.get("/foo", headers=headers)
    assert res.status_code == status.HTTP_200_OK


def test_invalid_auth() -> None:
    headers = {"Authorization": f"Bearer {id_token}-test"}
    res = client.get("/foo", headers=headers)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_user() -> None:
    auth.delete_user(test_username, test_password)
