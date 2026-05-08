from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from typing import Optional


def generate_access_token(identity: str or int, additional_claims: Optional[dict] = None) -> str:
    return create_access_token(identity=str(identity), additional_claims=additional_claims)


def generate_refresh_token(identity: str or int) -> str:
    return create_refresh_token(identity=str(identity))


def decode_jwt_token(token: str) -> dict:
    return decode_token(token)
