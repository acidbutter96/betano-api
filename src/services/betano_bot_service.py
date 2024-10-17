import undetected_chromedriver as uc
import time


class BetanoBotService:
    def __init__(self, url: str = "https://br.betano.com"):
        self.options = uc.ChromeOptions()
        self.options.headless = True

        self.driver = uc.Chrome(
            use_subprocess=True,
            headless=True,
            # options=self.options,
        )
        self.driver.get(url)
        time.sleep(20)
        self.driver.save_screenshot('nowsecure.png')
        time.sleep(10)
