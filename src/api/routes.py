from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
def test():
    return {"message": "Hello, World!"}


@router.post(
    "/login",
    description="Login endpoint",
)
def login():
    return {"message": "Login successful"}


@router.get(
    "/get_bets",
)
def get_bets():
    return {"message": "Retrieved bets", "list": []}
