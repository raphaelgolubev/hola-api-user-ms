from typing import Annotated
from fastapi import Depends

from src.api.service import UserService
from src.utils.security import Security


def get_register_service() -> UserService:
    security = Security()
    service = UserService(security=security)
    return service


RegisterServiceDep = Annotated[UserService, Depends(get_register_service)]