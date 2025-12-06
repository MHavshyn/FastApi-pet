from pydantic import BaseModel


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    expired_at: int
    token_type: str = "Bearer"
