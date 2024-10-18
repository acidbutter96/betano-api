# import undetected_chromedriver as uc
import asyncio
import json
from playwright.async_api import async_playwright


class BetanoBotService:
    def __init__(self, url: str = "https://br.betano.com"):
        with open('src/services/headers.json') as f:
            self.headers = json.load(f)
            # print(f"Headers: {self.headers}")

        self.url = url

    async def get_session_and_print(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--ignore-certificate-errors",
                    "--disable-gpu",
                    "--disable-software-rasterizer",
                ],
            )
            context = await browser.new_context(
                ignore_https_errors=True,
                extra_http_headers=self.headers,
            )
            page = await context.new_page()
            await page.goto(self.url)
            await asyncio.sleep(2)  # Non-blocking sleep

            # Click login button
            await page.click('xpath=//button[@data-qa="login-button"]')
            await asyncio.sleep(2)

            # Take screenshot and print title
            await page.screenshot(path="example.png")
            title = await page.title()
            print(f"Page Title: {title}")

            await browser.close()
            return {"title": title, "status": "Login successful"}
