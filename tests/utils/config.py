import os

from dotenv import load_dotenv

from cognito_pyauth import Config

load_dotenv(".env.test")

config = Config(
    region=os.getenv("AWS_DEFAULT_REGION", ""),
    pool_id=os.getenv("AWS_USER_POOL_ID", ""),
    client_id=os.getenv("AWS_USER_POOL_CLIENT_ID", ""),
)
