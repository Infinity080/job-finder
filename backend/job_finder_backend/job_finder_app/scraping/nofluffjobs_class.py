from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

class NoFluffJobs():
    def __init__(self) -> None:
        self._setup_browser()
        self.name = "nofluffjobs.com"

    def _setup_browser(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def _get_soup(self, url="https://nofluffjobs.com/pl") -> None:
        self.driver.get(url)
        self.driver.implicitly_wait(1)
        try:
            cookies_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Akceptuj')]")
            cookies_button.click()
            time.sleep(random.uniform(0.5, 1))
        except:
            print("No cookies for you")
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")

    def get_specializations(self) -> list[str]:
        self._get_soup()
        
        anchors = self.soup.select('a[href^="/pl/"]')
        ignore_prefixes = [
            "/pl/favourites", "/pl/mysalary", "/pl/companies", "/pl/profile",
            "/pl/log", "/pl/subscribe", "/pl/employers", "/pl/events",
            "/pl/personal-data-processing"
        ]
        results = []
        for a in anchors:
            href = a.get("href", "")
            text = a.get_text(strip=True)
            if (
                text and
                href.startswith("/pl/") and
                len(href.strip("/").split("/")) == 2 and
                not any(href.startswith(bad) for bad in ignore_prefixes)
            ):
                results.append(text)

        return results


    def _scrape_links(self, specializations: list[str], exp_level: str | None = None) -> dict[str, list[str]]:
        all_spec_links = self.get_specializations()
        refactor = {
            name.lower(): name.lower().replace(" ", "-").replace(".", "").replace("/", "-")
            for name in all_spec_links
        }

        results = {}

        for name in specializations:
            key = name.lower()
            if key not in refactor:
                continue

            p = refactor[key]
            base_url = f"https://nofluffjobs.com/pl/{p}"
            criteria = [f"category={p}"]
            if exp_level:
                criteria.append(f"seniority={exp_level}")
            full_url = f"{base_url}?criteria=" + "%20".join(criteria)

            self.driver.get(full_url)
            time.sleep(2)

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='/pl/job/']"))
                )
            except:
                results[name] = []
                continue

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            job_links = [
                "https://nofluffjobs.com" + a["href"]
                for a in soup.select("a[href^='/pl/job/']")
                if a.get("href")
            ]

            results[name] = job_links

        return results

    def get_links(self, specializations=None, exp_level=None) -> list[dict]:
        return self._scrape_links(specializations or [], exp_level)

if __name__ == "__main__":
    scraper = NoFluffJobs()
    jobs = scraper.get_links(["AI/ML", "Mobile"], "mid")
    print(jobs)
