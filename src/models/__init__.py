from pydantic import BaseModel, NameEmail


class BetanoLoginRequest(BaseModel):
    email: NameEmail
    password: str
