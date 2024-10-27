import logging
import json
import time

from utils import create_login_file  # , read_login_file
from playwright.sync_api import Browser


with open("./headers.json", "r") as f:
    headers = json.load(f)


def process(
    body: bytes,
    browser: Browser,
    job_id: str | None = None,
) -> None:
    url = body.decode()
    with browser.new_context(
        ignore_https_errors=True,
        extra_http_headers=headers,
    ) as ctx:
        with ctx.new_page() as page:
            page.goto(url)

            get_cookies_path = 'xpath=/html/body/div[2]/div[2]/div/div/div[2]/div/div/button[1]'  # noqa

            if accept_cookies := page.query_selector(get_cookies_path):
                accept_cookies.click()
                time.sleep(1)

            title = page.title()
            page.screenshot(path="entry-page.png")
            logging.info(f"Title of {url!r} is {title!r}")
            time.sleep(5)
            # click on button login

            logging.info("Click in login")
            x_path_login_button = 'xpath=/html/body/div[1]/div[1]/div/header/div/div[2]/button[1]'  # noqa
            login_button = page.query_selector(x_path_login_button)
            login_button.wait_for_element_state("visible")
            login_button.click()
            logging.info("Clicked, print the screen")
            page.screenshot(path="login-menu.png")

            time.sleep(2)

            logging.info(f"Entering email {'marcos.teste@example.com'}")
            x_path_email_field = 'xpath=/html/body/div[1]/div[1]/div/div[2]/div[1]/form/div[1]/div/input'  # noqa
            login_email_field = page.query_selector(
                x_path_email_field,
            )
            logging.info(f"Adding email to {login_email_field}")

            try:
                login_email_field.wait_for_element_state("visible")
                login_email_field.click()
                login_email_field.fill(
                    "marcospap96@gmail.com",
                    timeout=1000,
                )
            except Exception as ex:
                logging.error(f"Error clicking login button: {ex}")
            page.screenshot(path="login-menu-email.png")

            time.sleep(2)

            logging.info("Entering password")
            x_path_password_field = 'xpath=/html/body/div[1]/div[1]/div/div[2]/div[1]/form/div[2]/div/input'  # noqa
            password_email_field = page.query_selector(
                x_path_password_field,
            )
            logging.info(f"Adding password to {password_email_field}")

            try:
                password_email_field.wait_for_element_state("visible")
                password_email_field.click()
                password_email_field.fill("Popo.439053", timeout=1000,)
            except Exception as ex:
                logging.error(f"Error clicking login button: {ex}")
            page.screenshot(path="login-menu-password.png")

            time.sleep(2)

            logging.info("Clicking in login button")

            x_path_login_button = 'xpath=//*[@id="login-modal-submit"]'
            page.wait_for_selector(x_path_login_button)
            login_button = page.locator(x_path_login_button)
            try:
                login_button.click()
            except Exception as ex:
                logging.error(f"Error clicking login button: {ex}")
            time.sleep(20)
            page.screenshot(path="logged-in.png")

            storage_state = ctx.storage_state()
            local_storage = storage_state.get('origins', [])

            # Extract local storage for the specific origin if it exists
            for origin in local_storage:
                if origin['origin'] == 'https://superbet.com':
                    user = list(filter(lambda x: x['name'] == 'user', origin['localStorage']))  # noqa
                    logging.info("User data: %s", user)
                    create_login_file(user)
                    break

            time.sleep(5)

            page.goto("https://superbet.com/en-br/sport-bets/football/today")
            time.sleep(5)

            football_button_xpath = 'xpath=/html/body/div[1]/div[1]/div/div[1]/div[1]/div/div/div[2]/button[1]'  # noqa
            page.wait_for_selector(football_button_xpath)
            football_button = page.locator(football_button_xpath)
            football_button.click()
            time.sleep(200)
