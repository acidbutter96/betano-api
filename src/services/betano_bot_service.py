import undetected_chromedriver as uc
import time


class BetanoBotService:
    def __init__(self, url: str = "https://br.betano.com"):
        self.driver = uc.Chrome(
            headless=True,
            use_subprocess=False,
            version_main=127,
        )
        self.driver.get(url)
        self.driver.save_screenshot('nowsecure.png')
        time.sleep(10)
