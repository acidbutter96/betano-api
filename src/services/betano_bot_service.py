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
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    async def start_playwright(self):
        self.playwright = await async_playwright().start()

    async def stop_playwright(self):
        if self.playwright:
            await self.playwright.stop()

    async def get_session_and_print(self):
        # Certifique-se de que o Playwright foi iniciado
        if not self.playwright:
            raise RuntimeError("Playwright não foi inicializado. Chame 'start_playwright()' primeiro.")

        browser = await self.playwright.chromium.launch(
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

        try:
            await page.goto(self.url)
            await asyncio.sleep(2)  # Non-blocking sleep

            # Fazendo um screenshot da página
            await page.screenshot(path="example.png")
            title = await page.title()
            print(f"Page Title: {title}")

            return {"title": title, "status": "Login successful"}
        finally:
            # Fechando o navegador e liberando recursos
            await browser.close()


betano_service = BetanoBotService()
