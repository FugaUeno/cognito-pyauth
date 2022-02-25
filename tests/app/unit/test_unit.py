from cognito_pyauth import Auth
from tests.testutil import logger  # noqa: F401
from tests.testutil import config, token


def test_init() -> None:
    auth = Auth(config)

    assert auth is not None


def test_get_payload() -> None:
    auth = Auth(config)

    payload = auth.get_payload(token)
    assert payload.username == "test"
