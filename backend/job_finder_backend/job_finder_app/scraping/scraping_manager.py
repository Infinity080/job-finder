from job_finder_app.scraping.pracuj_class import Pracuj 
from job_finder_app.scraping.justjoinit_class import JustJoinIt 
from job_finder_app.scraping.nofluffjobs_class import NoFluffJobs 
from job_finder_app.models import Specialization, Website

class ScrapingManager():
    def __init__(self) -> None:
        self.pracuj = Pracuj()
        self.justJoinIt = JustJoinIt()
        self.nofluffjobs = NoFluffJobs()

        self.websites = [self.pracuj, self.justJoinIt, self.nofluffjobs]

        self.domain_to_scraper = {
            "pracuj.pl": self.pracuj,
            "justjoin.it": self.justJoinIt,
            "nofluffjobs.com" : self.nofluffjobs
        }

    def get_all_specializations(self):
        specs = {}
        for website in self.websites:
            db_website, _ = Website.objects.get_or_create(name=website.name)
            website_specs = Specialization.objects.filter(website=db_website)

            if website_specs.exists():
                specs[website.name] = [s.name for s in website_specs]
            else:
                scraped_specs = website.get_specializations()
                for spec_name in scraped_specs:
                    Specialization.objects.get_or_create(name=spec_name, website=db_website)
                specs[website.name] = scraped_specs
        return specs



    def get_jobs_by_specialization(self, specializations, exp_level):
        links = {}
        for website in self.websites:
            db_website = Website.objects.get(name=website.name)
            valid_specs = Specialization.objects.filter(website=db_website).values_list("name", flat=True)

            site_specs = [spec for spec in specializations if spec in valid_specs]

            if site_specs:
                links[website.name] = website.get_links(site_specs, exp_level)
        return links

    def scrape_listing_text(self, url):
        for domain, scraper in self.domain_to_scraper.items():
            if domain in url:
                return scraper.scrape_listing_text(url)
        raise ValueError(f"No scraper available for URL: {url}")
   
if __name__ == "__main__":
    test = ScrapingManager()
