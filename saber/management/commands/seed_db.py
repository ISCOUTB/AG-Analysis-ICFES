from django.core.management.base import BaseCommand, CommandParser, CommandError
import pandas as pd
import dask.dataframe as dd
from django.conf import settings
import os
import uuid
import gc
from typing import Literal
import logging


COLOMBIA_DEPARTMENTS: list[str] = ['BOGOTÁ', 'VALLE', 'TOLIMA', 'SANTANDER', 'SUCRE', 'ANTIOQUIA',
                                   'BOYACA', 'CAUCA', 'HUILA', 'CUNDINAMARCA', 'CORDOBA', 'ATLANTICO',
                                   'BOLIVAR', 'ARAUCA', 'NORTE SANTANDER', 'CALDAS', 'RISARALDA',
                                   'CESAR', 'QUINDIO', 'MAGDALENA', 'CHOCO', 'LA GUAJIRA', 'META',
                                   'CAQUETA', 'NARIÑO', 'PUTUMAYO', 'AMAZONAS', 'CASANARE',
                                   'SAN ANDRES', 'GUAVIARE', 'GUAINIA', 'VAUPES', 'VICHADA']


logger: logging.Logger = logging.getLogger('saber')


class Command(BaseCommand):
    help = 'Populate the database with the data'

    DATA_DIR = os.path.join(settings.BASE_DIR, "data")

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-Ft', '--file-type',
                            choices=['Saber11', 'SaberPro'],
                            nargs='?',
                            default='Saber11',
                            help='File to be procesed')

    def add_departments(self) -> None:
        from saber.models import Department

        logger.info('Adding the Departments ...')

        for department in COLOMBIA_DEPARTMENTS:
            if Department.objects.get(name=department):
                continue

            department: Department = Department.objects.create(name=department)

            logger.info(f"Department created | id: {department.id}")

        logger.info('Finished adding the Departments')

    def parse_row(self, row: pd.Series) -> None:
        from saber.models import Department, Municipality

        if self.type == 'Saber11':
            from saber.models import Highschool

            department, municipality, establishment, period = row[[
                'COLE_DEPTO_UBICACION', 'COLE_MCPIO_UBICACION', 'COLE_NOMBRE_ESTABLECIMIENTO', 'PERIODO']]

            department_object = Department.objects.get(name=department)

            if not department_object:
                logger.fatal(f"Department not found | name: {department}")
                raise CommandError()

            municipality_object, _ = Municipality.objects.get_or_create(
                name=municipality, department=department_object)

            highschool_object = Highschool.objects.get_or_create(
                name=establishment, municipality=municipality_object)

            return

    def parse_dataframe(self) -> None:
        df: pd.DataFrame = dd.read_csv(os.path.join(self.DATA_DIR, f"{self.cleaned_file_name}.csv"),
                                       dtype='str',
                                       assume_missing=True,
                                       na_values=['', 'NA', 'nan']).compute()

        df.apply(self.parse_row, axis=1)

    def clean_dataframe(self, file_path: str) -> None:
        logger.info('Reading ...')

        df: pd.DataFrame = dd.read_csv(file_path,
                                       dtype='str',
                                       assume_missing=True,
                                       na_values=['', 'NA', 'nan']).compute()

        logger.info('Finished reading the DataFrame')

        self._cleaned_file_name = uuid.uuid4()

        logger.info('Doing some more cleaning/replacing values')

        if self.type == 'Saber11':
            df = df[df['ESTU_PAIS_RESIDE'] == 'COLOMBIA']
            df['COLE_DEPTO_UBICACION'] = df['COLE_DEPTO_UBICACION'].replace(
                {'BOGOTA': 'BOGOTÁ'})

        if self.type == 'SaberPro':
            df = df[df['ESTU_PAIS_RESIDE'] == 'COLOMBIA']
            df = df[df['ESTU_DEPTO_RESIDE'].isin(COLOMBIA_DEPARTMENTS)]

        df = df.dropna(ignore_index=True)

        logger.info('Exporting ...')

        df.to_csv(os.path.join(self.DATA_DIR, f"""{
                  self.cleaned_file_name}.csv"""), index=False)

        del df
        gc.collect()

    def handle(self, *args, **options):
        file_type: str = options['file_type']

        if not file_type in ['Saber11', 'SaberPro']:
            logger.fatal("Invalid file type")
            return

        if file_type == 'Saber11':
            csv_file: str = os.path.join(self.DATA_DIR, "Resultados11.csv")
            self._type = 'Saber11'

        if file_type == 'SaberPro':
            csv_file: str = os.path.join(self.DATA_DIR, "ResultadosPro.csv")
            self._type = 'SaberPro'

        if not os.path.exists(csv_file):
            logger.fatal('File not found')
            return

        logger.info('Started cleaning the DataFrame')

        self.clean_dataframe(file_path=csv_file)

        self.add_departments()

        logger.info(f"DataFrame cleaned and stored as '{
                    self.cleaned_file_name}.csv'")

        logger.info('Started Parsing ...')

        self.parse_dataframe()

        logger.info('Removing the file')

        os.remove(os.path.join(self.DATA_DIR, f"{self.cleaned_file_name}.csv"))

        logger.info('Finished')

    @property
    def cleaned_file_name(self) -> str:
        return self._cleaned_file_name

    @property
    def type(self) -> Literal['Saber11', 'SaberPro']:
        return self._type
