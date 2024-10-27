def create_login_file(data: str) -> bool:
    try:
        with open("login.json", "w+") as file:
            file.write(data)
        return True
    except Exception:
        return False


def read_login_file() -> str | None:
    try:
        with open("login.json", "r") as file:
            return file.read()
    except FileNotFoundError:
        return None
