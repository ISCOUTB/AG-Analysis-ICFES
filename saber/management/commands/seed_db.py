from django.core.management.base import BaseCommand, CommandParser
import pandas as pd
import dask.dataframe as dd
from django.conf import settings
import os
import uuid
import gc
from typing import Literal


depto_col: list[str] = ['BOGOTÁ', 'VALLE', 'TOLIMA', 'SANTANDER', 'SUCRE', 'ANTIOQUIA',
                        'BOYACA', 'CAUCA', 'HUILA', 'CUNDINAMARCA', 'CORDOBA', 'ATLANTICO',
                        'BOLIVAR', 'ARAUCA', 'NORTE SANTANDER', 'CALDAS', 'RISARALDA',
                        'CESAR', 'QUINDIO', 'MAGDALENA', 'CHOCO', 'LA GUAJIRA', 'META',
                        'CAQUETA', 'NARIÑO', 'PUTUMAYO', 'AMAZONAS', 'CASANARE',
                        'SAN ANDRES', 'GUAVIARE', 'GUAINIA', 'VAUPES', 'VICHADA']


class Command(BaseCommand):
    help = 'Populate the database with the data'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-Ft', '--file-type',
                            choices=['Saber11', 'SaberPro'],
                            nargs='?',
                            default='Saber11',
                            help='File to be procesed')

    def clean_dataframe(self, file_path: str) -> None:
        self.stdout.write(self.style.HTTP_INFO('[ Info ] Reading ...'))

        df: pd.DataFrame = dd.read_csv(file_path,
                                       dtype='str',
                                       assume_missing=True,
                                       na_values=['', 'NA', 'nan']).compute()

        self.stdout.write(self.style.SUCCESS(
            '[ Info ] Finished reading the DataFrame'))

        self._cleaned_file_name = uuid.uuid4()

        if self.type == 'Saber11':
            df = df[df['ESTU_PAIS_RESIDE'] == 'COLOMBIA']
            df['COLE_DEPTO_UBICACION'] = df['COLE_DEPTO_UBICACION'].replace(
                {'BOGOTA': 'BOGOTÁ'})

        if self.type == 'SaberPro':
            df = df[df['ESTU_PAIS_RESIDE'] == 'COLOMBIA']
            df = df[df['ESTU_DEPTO_RESIDE'].isin(depto_col)]

        df = df.dropna(ignore_index=True)

        self.stdout.write(self.style.HTTP_INFO('[ Info ] Exporting ...'))

        df.to_csv(os.path.join(settings.BASE_DIR, "data",
                  f"{self.cleaned_file_name}.csv"), index=False)

        del df
        gc.collect()

    def handle(self, *args, **options):
        file_type: str = options['file_type']

        if not file_type in ['Saber11', 'SaberPro']:
            self.stdout.write(self.style.ERROR("[ Error ] Invalid file type"))
            return

        if file_type == 'Saber11':
            csv_file: str = os.path.join(
                settings.BASE_DIR, "data", "Resultados11.csv")
            self._type = 'Saber11'

        if file_type == 'SaberPro':
            csv_file: str = os.path.join(
                settings.BASE_DIR, "data", "ResultadosPro.csv")
            self._type = 'SaberPro'

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR('[ Error ] File not found'))
            return

        self.stdout.write(self.style.HTTP_INFO(
            '[ Info ] Started cleaning the DataFrame'))

        self.clean_dataframe(file_path=csv_file)

        self.stdout.write(self.style.SUCCESS(
            f"[ Info ] DataFrame cleaned and stored as {self.cleaned_file_name}.csv"))

    @property
    def cleaned_file_name(self) -> str:
        return self._cleaned_file_name

    @property
    def type(self) -> Literal['Saber11', 'SaberPro']:
        return self._type
