from typing import Any
from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int

class APIResponse(BaseModel):
    data: Any = None
    status: int = 200,
    details: str = 'Operation successfully'