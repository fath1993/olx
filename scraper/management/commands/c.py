from django.core.management.base import BaseCommand

from scraper.scrapers import ejobs


class Command(BaseCommand):
    def handle(self, *args, **options):
        ejobs()