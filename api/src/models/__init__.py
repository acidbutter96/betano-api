from pydantic import BaseModel, NameEmail


class SuperBetLoginRequest(BaseModel):
    email: NameEmail
    password: str
