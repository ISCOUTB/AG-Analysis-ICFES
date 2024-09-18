from django.core.management.base import BaseCommand, CommandParser
from saber.models import Department, Municipality, Highschool, HighschoolStudent
import pandas as pd
import dask.dataframe as dd
from django.conf import settings
from typing import Literal
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import logging
import os
import uuid
import gc


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
    skip_municipalities = False
    skip_highschools = False

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-Ft', '--file-type',
                            choices=['Saber11', 'SaberPro'],
                            help='File to be procesed')

    def read_dataframe(self, file_path: str) -> pd.DataFrame:
        return dd.read_csv(file_path,
                           dtype='str',
                           assume_missing=True,
                           na_values=['', 'NA', 'nan']).compute()

    def add_departments(self) -> None:
        logger.info('Adding the Departments ...')

        for department in COLOMBIA_DEPARTMENTS:
            Department.objects.get_or_create(name=department)

        logger.info('Finished adding the Departments')

    def parse_row(self, row: pd.Series) -> None:

        if self.type == 'Saber11':

            if not self.skip_municipalities and Municipality.objects.filter(department=None).exists():
                self.skip_municipalities = True

            if not self.skip_highschools and Highschool.objects.filter(municipality=None).exists():
                self.skip_highschools = True

            if self.skip_municipalities and self.skip_highschools:
                return

            department_name, municipality_name, establishment_name = row[[
                'COLE_DEPTO_UBICACION', 'COLE_MCPIO_UBICACION', 'COLE_NOMBRE_ESTABLECIMIENTO']]

            department = Department.objects.get(name=department_name)
            municipality = Municipality.objects.get(name=municipality_name)
            highschool = Highschool.objects.get(name=establishment_name)

            if not self.skip_municipalities:
                municipality.department = department
                municipality.save()

            if not self.skip_highschools:
                highschool.municipality = municipality
                highschool.save()

            return

    def parse_students(self) -> None:
        df: pd.DataFrame = self.read_dataframe(file_path=os.path.join(
            self.DATA_DIR, f"{self.cleaned_file_name}.csv"))

        if self.type == 'Saber11':

            students = [
                HighschoolStudent(
                    PUNT_ENGLISH=punt_english,
                    PUNT_MATHEMATICS=punt_math,
                    PUNT_SOCIAL_CITIZENSHIP=punt_social,
                    PUNT_NATURAL_SCIENCES=punt_natural,
                    PUNT_CRITICAL_READING=punt_languaje,
                    PUNT_GLOBAL=punt_global,
                    highschool=Highschool.objects.get(name=highschool_name),
                    period=period,
                    genre="MALE" if genre == 'M' else 'FEMALE'
                ) for punt_english, punt_math, punt_social, punt_natural, punt_languaje, punt_global, period, highschool_name, genre in df[[
                    'PUNT_INGLES', 'PUNT_MATEMATICAS', 'PUNT_SOCIALES_CIUDADANAS', 'PUNT_C_NATURALES', 'PUNT_LECTURA_CRITICA', 'PUNT_GLOBAL', 'PERIODO', 'COLE_NOMBRE_ESTABLECIMIENTO', 'ESTU_GENERO']].values]

            HighschoolStudent.objects.bulk_create(students)

            return

    def parse_dataframe(self) -> None:

        df: pd.DataFrame = self.read_dataframe(file_path=os.path.join(
            self.DATA_DIR, f"{self.cleaned_file_name}.csv"))

        if self.type == 'Saber11':
            HighschoolStudent.objects.all().delete()

            def create_municipalities():
                for name in df['COLE_MCPIO_UBICACION'].unique():
                    Municipality.objects.get_or_create(name=name)

            def create_highschools():
                for name in df['COLE_NOMBRE_ESTABLECIMIENTO'].unique():
                    Highschool.objects.get_or_create(name=name)

            with ThreadPoolExecutor() as executor:
                executor.submit(create_municipalities)
                executor.submit(create_highschools)

        df.apply(self.parse_row, axis=1)

    def clean_dataframe(self, file_path: str) -> None:
        logger.info('Reading ...')

        df: pd.DataFrame = self.read_dataframe(file_path=file_path)

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

        logger.info('Started Parsing students ...')

        self.parse_students()

        logger.info('Removing the file')

        os.remove(os.path.join(self.DATA_DIR, f"{self.cleaned_file_name}.csv"))

        logger.info('Finished')

    @property
    def cleaned_file_name(self) -> str:
        return self._cleaned_file_name

    @property
    def type(self) -> Literal['Saber11', 'SaberPro']:
        return self._type
