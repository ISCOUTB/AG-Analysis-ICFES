from django.core.management.base import BaseCommand, CommandParser
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Populate the database with the data'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-Ft', '--file-type',
                            choices=['Saber11', 'SaberPro'],
                            nargs='?',
                            default='Saber11',
                            help='File to be procesed')

        parser.add_argument('-C', '--chunksize', type=int, nargs='?',
                            default=100000, help='Chunksize to be used')

    def handle(self, *args, **options):
        file_type: str = options['file_type']

        if file_type == 'Saber11':
            csv_file: str = os.path.join(
                settings.BASE_DIR, "data", "Resultados11.csv")

        if file_type == 'SaberPro':
            csv_file: str = os.path.join(
                settings.BASE_DIR, "data", "ResultadosPro.csv")

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR('[ Error ] File not found'))

        chunksize: int = options['chunksize']

        num_threads: int | None = os.cpu_count()

        data_iterator = pd.read_csv(csv_file, chunksize=chunksize)

        self.stdout.write(self.style.HTTP_INFO(
            f"[ Info ] Using ( Threads ) ( {num_threads} )"))

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map('', data_iterator)
