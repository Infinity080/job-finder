from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from lxml import etree

class JustJoinIt():
    def __init__(self) -> None:
        self._setup_browser()
        self.default_url = "https://justjoin.it/job-offers/all-locations/"
        self.name = "justjoin.it"

    def _setup_browser(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    def _get_soup(self, url) -> None:
        self.driver.get(url)
        self.driver.implicitly_wait(1)
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")
 
    def _scrape_links(self,specializations,exp_level):
        links = {}
        for specialization in specializations:
            new_url = self.default_url+f"{specialization}?experience-level={exp_level}"
            self._get_soup(new_url)
            spec_links = []

            job_links = self.soup.find_all('a', href=lambda href: href and href.startswith('/job-offer/'))

            if not job_links:
                continue  
                
            for link in job_links:
                href = link.get("href")
                listing_url = "https://www.justjoin.it" + href 
                if href:
                    spec_links.append(listing_url)  
            
                    
            links[specialization] = spec_links
        
        return links


    def get_links(self,specializations,exp_level):
        self.links = self._scrape_links(specializations,exp_level)
        return self.links


    def get_specializations(self) -> list[str]:
        categories_xml = 'https://s3.eu-west-1.amazonaws.com/public.justjoin.com/justjoinit/sitemaps/categories/part0.xml'
        self.driver.get(categories_xml)
        xml_content = self.driver.page_source

        tree = etree.fromstring(xml_content)
        
        categories = [loc.text.split("/")[-1] for loc in tree.findall('.//ns:loc', {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'})]
        return categories


test = JustJoinIt()     