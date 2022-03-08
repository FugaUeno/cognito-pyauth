from cognito_pyauth import Auth
from tests.testutil import logger  # noqa: F401
from tests.testutil import config


def test_init() -> None:
    auth = Auth(config)

    assert auth is not None
