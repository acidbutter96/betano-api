import json
import time

from playwright.sync_api import Browser, Page
from settings import env


with open("./worker/headers.json", "r") as f:
    headers = json.load(f)


def get_competitions_and_tournaments(page: Page):
    # Create dictionary for competitions, tournaments, and XPaths
    competition_data = []

    # Locate each competition element
    competition_cards = page.locator('//div[contains(@class, "sport-competition-card sport-competition-item")]')
    competition_count = competition_cards.count()

    for i in range(competition_count):
        # Select each competition card
        card = competition_cards.nth(i)

        card.click()
        time.sleep(1)

        competition_name_element = card.locator('//span[contains(@class, "category-name e2e-competition")]')
        competition_name = competition_name_element.inner_text() if competition_name_element.count() > 0 else "N/A"

        # Locate the 'main' element within the card with class 'tournaments'
        tournaments_main = card.locator('main.tournaments')

        # Retrieve each tournament element inside the tournaments main
        tournaments = tournaments_main.locator('//div[contains(@class, "tournament e2e-competition-tournament")]')
        tournament_count = tournaments.count()

        # List to hold data about tournaments within this competition card
        tournament_data = []

        # print(tournaments.nth(0).evaluate('node => node.getXPath()'))

        for j in range(tournament_count):
            # Select each tournament div and retrieve its XPath
            tournament = tournaments.nth(j)

            # Retrieve tournament name from within the tournament div
            tournament_name = tournament.locator('//div[contains(@class, "tournament-name")]').inner_text()

            # Append tournament data to the list
            tournament_data.append({
                "tournament_name": tournament_name,
            })

        card.click()
        time.sleep(1)

        # Append competition card data, including tournaments, to the main data list
        competition_data.append({
            "card_index": i,
            "competition_name": competition_name,
            "tournaments": tournament_data
        })

    return competition_data


def task_pull_active_tournaments(
    payload,
    browser: Browser,
    job_id: str,
):
    with browser.new_context(
        ignore_https_errors=True,
        extra_http_headers=headers
    ) as ctx:
        with ctx.new_page() as page:
            page.goto(f"{env.URL}/sport-bets/football/competitions")
            page.wait_for_load_state(state="domcontentloaded")

            get_cookies_path = 'xpath=/html/body/div[2]/div[2]/div/div/div[2]/div/div/button[1]'  # noqa

            if accept_cookies := page.query_selector(get_cookies_path):
                accept_cookies.click()
                time.sleep(1)

            data = get_competitions_and_tournaments(page)

            with open("./saved_tournaments/tournaments.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
