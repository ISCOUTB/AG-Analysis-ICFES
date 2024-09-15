# ! Not using this


from django.core.management.base import BaseCommand, CommandParser
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import pandas as pd
import os
from django.conf import settings
from pandas.io.parsers import TextFileReader
import multiprocessing
import numpy as np


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

    def clean_chunk(self, df: pd.DataFrame) -> None:
        df = df.dropna()
        df = df.drop_duplicates()

        return df

    def process_chunk(self, chunk: pd.DataFrame) -> None:
        with ThreadPoolExecutor() as executor:
            sub_chunks = np.array_split(chunk, os.cpu_count())
            cleaned_sub_chunks = list(
                executor.map(self.clean_chunk, sub_chunks))

        cleaned_chunk = pd.concat(cleaned_sub_chunks)

        self.stdout.write(self.style.SUCCESS(
            f'Processed chunk of size {len(cleaned_chunk)}'))

    def handle(self, *args, **options):
        file_type: str = options['file_type']

        if file_type == 'Saber11':
            csv_file: str = os.path.join(
                settings.BASE_DIR, "data", "Resultados11.csv")

        elif file_type == 'SaberPro':
            csv_file: str = os.path.join(
                settings.BASE_DIR, "data", "ResultadosPro.csv")

        else:
            self.stdout.write(self.style.ERROR("[ Error ] Invalid file type"))
            return

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR('[ Error ] File not found'))
            return

        chunksize: int = options['chunksize']
        num_processes: int = multiprocessing.cpu_count()

        self.stdout.write(self.style.HTTP_INFO(
            f"[ Info ] Using {num_processes} processes"))

        data_iterator: TextFileReader = pd.read_csv(
            csv_file, chunksize=chunksize)

        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            executor.map(self.process_chunk, data_iterator)

        self.stdout.write(self.style.SUCCESS(
            '[ Success ] Processing completed'))    
