from playwright.sync_api import Page
from settings import env
import json


with open("./worker/headers.json", "r") as f:
    headers = json.load(f)


def create_login_file(cookies: list) -> bool:
    try:
        for cookie in cookies:
            if cookie.get("name") == "user":
                with open("login.json", "w+") as file:
                    file.write(cookie.get("value"))
            return True
    except Exception:
        return False


def login_assistant(page: Page,) -> bool:
    user_data = read_login_file()

    # context = browser.new_context(
    #     ignore_https_errors=True,
    #     extra_http_headers=headers,
    # )
    # page = context.new_page()

    try:
        with open("storage_state.json", "r") as f:
            storage = json.load(f)

        # Modify the storage state JSON to add localStorage
        with open("storage_state.json", "r") as f:
            storage = json.load(f)

        # Find the origin for "https://superbet.com" or add it if it doesn't exist
        origin = env.URL
        local_storage = next(
            (entry for entry in storage.get("origins", []) if entry["origin"] == origin),
            None,
        )

        if local_storage is None:
            local_storage = {"origin": origin, "localStorage": []}
            storage["origins"].append(local_storage)

        # Add or update the 'user' key in localStorage
        local_storage["localStorage"].append(
            {"name": "user", "value": json.dumps(user_data)}
        )

        # Save the modified storage state
        with open("storage_state.json", "w") as f:
            json.dump(storage, f)

        # Load the modified storage state into a new browser context
        # new_context = browser.new_context(storage_state="storage_state.json")
        # new_page = new_context.new_page()

        # # Navigate to the site to ensure localStorage is available
        # new_page.goto("https://superbet.com")
        # value = new_page.evaluate("() => localStorage.getItem('user')")

        return True
    except Exception as e:
        print(f"Error setting user data in localStorage: {e}")
        return False


def read_login_file() -> str | None:
    try:
        with open("login.json", "r") as file:
            return file.read()
    except FileNotFoundError:
        return None
