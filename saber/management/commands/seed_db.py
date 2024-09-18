from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populate the database with the data'

    def handle(self, *args, **options):
        self.stdout.write('Seed was called')
