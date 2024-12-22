from dataclasses import dataclass
from typing import Any, Dict

import jwt
import jwt.warnings

from app.domain.entities.user import User
from app.domain.entities.user_id import UserId


@dataclass
class TokenPayloadDTO:
    sub: int
    email: str
    username: str


class JwtProcessor:
    def __init__(self, private_key: str, algorithm: str) -> None:
        self.private_key = private_key
        self.algorithm = algorithm

    def _encode_jwt(self, payload: Dict[str, Any]) -> str:
        encoded = jwt.encode(
            payload=payload,
            key=self.private_key,
            algorithm=self.algorithm
        )
        return encoded

    def _decode_jwt(self, token: str) -> TokenPayloadDTO:
        data = jwt.decode(
            jwt=token,
            key=self.private_key,
            algorithms=self.algorithm
        )
        return TokenPayloadDTO(
            sub=int(data["sub"]),
            email=data["email"],
            username=data["username"],
        )

    def create_token(
            self,
            user: User
    ) -> str:
        jwt_payload = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username
        }
        token = self._encode_jwt(jwt_payload)
        return token

    def validate_token(self, token: str) -> UserId:
        try:
            payload = self._decode_jwt(token)
            return UserId(payload.sub)
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
