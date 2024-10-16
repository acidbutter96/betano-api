import undetected_chromedriver as uc


class BetanoBotServie:
    def __init__(self,):
        self.driver = uc.Chrome(
            headless=True,
            use_subprocess=False,
        )
        self.driver.get('https://nowsecure.nl')
        self.driver.save_screenshot('nowsecure.png')
