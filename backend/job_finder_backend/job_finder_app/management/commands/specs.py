from django.core.management.base import BaseCommand
from job_finder_app.scraping.scraping_manager import ScrapingManager

class Command(BaseCommand):
    help = 'Run the scraping manager'

    def handle(self, *args, **kwargs):
        scraper = ScrapingManager()
        scraper.get_all_specializations()
        self.stdout.write(self.style.SUCCESS('Specializations set successfully.'))
        