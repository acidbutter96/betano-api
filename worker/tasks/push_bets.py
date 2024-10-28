import logging
import json
import time

from playwright.sync_api import Browser
from settings import env
from core import login_assistant


with open("./worker/headers.json", "r") as f:
    headers = json.load(f)


def task_push_bets(
    payload,
    browser: Browser,
    job_id: str,
):
    with browser.new_context(
        ignore_https_errors=True,
        extra_http_headers=headers,
        storage_state="storage_state.json"
    ) as ctx:
        ctx.storage_state(path="storage_state.json")
        with ctx.new_page() as page:
            if not login_assistant(browser):
                logging.error(f"Failed to login at job id: {payload.get('job_id')}")
                return
            page.reload()

            is_logged_in = page.evaluate("() => localStorage.getItem('user')")

            logging.info(f"Processing job id: {payload.get('job_id')} started - logged in")

            page.goto(env.URL)

            get_cookies_path = 'xpath=/html/body/div[2]/div[2]/div/div/div[2]/div/div/button[1]'  # noqa

            if accept_cookies := page.query_selector(get_cookies_path):
                accept_cookies.click()
                time.sleep(1)

            title = page.title()
            page.screenshot(path="already-logged.png")
            logging.info(f"Title of {env.URL!r} is {title!r}")
            time.sleep(50)
    # with login_assistant(browser) as ctx:
    #     with ctx.new_page() as page:
    #         logging.info(f"Processing job id: {payload.get('job_id')} started - logged in")

    #         get_cookies_path = 'xpath=/html/body/div[2]/div[2]/div/div/div[2]/div/div/button[1]'  # noqa

    #         if accept_cookies := page.query_selector(get_cookies_path):
    #             accept_cookies.click()
    #             time.sleep(1)

    #         title = page.title()
    #         page.screenshot(path="already-logged.png")
    #         logging.info(f"Title of {env.URL!r} is {title!r}")
    #         time.sleep(500)
