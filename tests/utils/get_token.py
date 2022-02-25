import json

import requests


def get_token() -> str:
    client_id = "4f8op3tmvkpt4n7sa1jmft64r6"
    username = "test"
    password = "Test_1234"
    region = "ap-northeast-1"

    res = requests.post(
        f"https://cognito-idp.{region}.amazonaws.com",
        headers={
            "Content-Type": "application/x-amz-json-1.1",
            "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
            "X-Amz-User-Agent": "python-requests",
        },
        data=json.dumps(
            {
                "AuthFlow": "USER_PASSWORD_AUTH",
                "ClientId": client_id,
                "AuthParameters": {
                    "USERNAME": username,
                    "PASSWORD": password,
                },
            }
        ),
    )
    return res.json()["AuthenticationResult"]["IdToken"]
