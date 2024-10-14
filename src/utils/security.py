from passlib.context import CryptContext
from src.config import settings

from src.interfaces import ISecurity


class Security(ISecurity):
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_value(self, password: str):
        return self.pwd_context.hash(password)

    def verify(self, plain: str, hash: str):
        return self.pwd_context.verify(plain, hash)