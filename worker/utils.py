from json import loads


def create_login_file(cookies: list) -> bool:
    try:
        for cookie in cookies:
            if cookie.get("name") == "user":
                with open("login.json", "w+") as file:
                    file.write(cookie.get("value"))
            return True
    except Exception:
        return False


def read_login_file() -> str | None:
    try:
        with open("login.json", "r") as file:
            return loads(file.read())
    except FileNotFoundError:
        return None
