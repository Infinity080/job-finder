from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
import json

class Pracuj():
    def __init__(self) -> None:
        self._setup_browser()
        self.name = "pracuj.pl"

    def _setup_browser(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    def _get_soup(self, url="https://it.pracuj.pl/praca/ostatnich%2024h;p,1?et=17%2C3%2C1") -> None:
        self.driver.get(url)
        self.driver.implicitly_wait(1)
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")
    
    def _scrape_links(self,specializations,exp_level):
        urls = {
            "junior" : "https://it.pracuj.pl/praca/ostatnich%2024h;p,1?et=17%2C3%2C1",
            "mid" : "https://it.pracuj.pl/praca/ostatnich%2024h;p,1?et=4",
            "senior" : "https://it.pracuj.pl/praca/ostatnich%2024h;p,1?et=18"
        }
        links = {}
        for specialization in specializations:
            spec = specialization
            if specialization == 'Big Data / Data Science':
                spec = 'big-data-science'
            page_url = urls[exp_level] + f"&its={spec.lower().replace(' ', '-').replace('&','-').replace('/','-')}"
            self._get_soup(page_url)
            spec_links = []
            while True:
                
                offers_list = self.soup.find("div", id="offers-list")
                if not offers_list:
                    break  
                
                job_links = offers_list.find_all("a", attrs={"data-test": "link-offer"})
                for link in job_links:
                    href = link.get("href")
                    if href:
                        spec_links.append(href)  
                
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, "[data-test='bottom-pagination-button-next']")
                    next_button.click()  
                    time.sleep(random.uniform(0.5,1))
                    
                except:
                    break
                    
            links[specialization] = spec_links
        
        return links
    
    """
    def scrape_listing_text(self, listing_url):
        self._get_soup(url=listing_url)

        main_points = {
            "experience_level": None,
            "employment_type": None,
            "job_form": None
        }

        scroll_mapping = {
            "position-levels": "experience_level",
            "work-modes": "employment_type",
            "work-schedules": "job_form"
        }

        for scroll_id, key in scroll_mapping.items():
            li = self.soup.find("li", {"data-scroll-id": scroll_id})
            if li:
                badge = li.find("div", {"data-test": "offer-badge-title"})
                if badge:
                    main_points[key] = badge.get_text(strip=True)

        technologies = []
        for section_id in ["technologies-expected-1", "technologies-optional-1"]:
            tech_section = self.soup.find("div", {"data-scroll-id": section_id})
            if tech_section:
                for li in tech_section.find_all("li"):
                    text = li.get_text(strip=True)
                    if text:
                        technologies.append(text)

        requirements = []
        accordion = self.soup.find("section", {"data-test": "section-requirements"})
        if accordion:
            for section_id in ["requirements-expected-1", "requirements-optional-1"]:
                block = accordion.find("div", {"data-scroll-id": section_id})
                if block:
                    for li in block.find_all("li"):
                        text = li.get_text(strip=True)
                        if text:
                            requirements.append(text)

        return {
            "experience_level": main_points["experience_level"],
            "employment_type": main_points["employment_type"],
            "job_form": main_points["job_form"],
            "technologies": technologies,
            "requirements": requirements
        }
    """
    def get_links(self,specializations,exp_level):
        self.links = self._scrape_links(specializations,exp_level)
        return self.links
        

    def get_specializations(self) -> list[str]:
        self._get_soup()
        script_tag = self.soup.find('script', string=lambda text: text and 'itSpecializations' in text)

        script_content = script_tag.string

        match = re.search(r'"itSpecializations"\s*:\s*(\[\{.*?\}\])', script_content, re.DOTALL)
        json_part = match.group(1)

        json_part = json_part.strip()

        site_json = json.loads(json_part)


        return [d.get('name') for d in site_json if d.get('name')]
if __name__ == "__main__":
    test = Pracuj()
