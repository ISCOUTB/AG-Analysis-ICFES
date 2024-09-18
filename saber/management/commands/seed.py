from typing import Literal, Any
from django.core.management.base import BaseCommand, CommandParser
from data.constants import COLOMBIA_DEPARTMENTS
from django.conf import settings
from django.db import transaction
from saber.models import Department, Municipality, Highschool, HighschoolStudent, College, CollegeStudent
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import dask.dataframe as dd
import os
import logging
import uuid
import sys

logger = logging.getLogger('saber')


class Command(BaseCommand):
    help = 'Populate the database with the data'

    DATA_DIR = os.path.join(settings.BASE_DIR, "data")

    # ! -----------------------------------------------------------------------------------------------------|>

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-Ft', '--file-type',
                            choices=['Saber11', 'SaberPro'],
                            help='File to be procesed')

    def read_dataframe(self, file_path: str) -> pd.DataFrame:
        return dd.read_csv(file_path,
                           dtype='str',
                           assume_missing=True,
                           na_values=['', 'NA', 'nan']).compute()

    def fill(self, data: pd.DataFrame) -> None:
        logger.info('( fill ) run')

        if self.type == 'Saber11':
            def fill_municipalities() -> None:
                logger.info('( fill_municipalities ) run')

                for name in data['COLE_MCPIO_UBICACION'].unique():
                    Municipality.objects.get_or_create(name=name)

            def fill_highschools() -> None:
                logger.info('( fill_highschools ) run')

                for name in data['COLE_NOMBRE_ESTABLECIMIENTO'].unique():
                    Highschool.objects.get_or_create(name=name)

            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                futures = [
                    executor.submit(fill_municipalities),
                    executor.submit(fill_highschools)
                ]

                for future in futures:
                    future.result()

            return

    # ! -----------------------------------------------------------------------------------------------------|>

    def clean_dataframe(self, file_path: str) -> None:
        logger.info('( clean_dataframe ) run')
        logger.info('( clean_dataframe ) Reading Dataframe')

        df: pd.DataFrame = self.read_dataframe(file_path=file_path)

        self._file_name = uuid.uuid4()

        logger.info('( clean_dataframe ) Cleaning some values')

        if self.type == 'Saber11':
            df = df[df['ESTU_PAIS_RESIDE'] == 'COLOMBIA']
            df['COLE_DEPTO_UBICACION'] = df['COLE_DEPTO_UBICACION'].replace(
                {'BOGOTA': 'BOGOTÁ'})

        if self.type == 'SaberPro':
            df = df[df['ESTU_PAIS_RESIDE'] == 'COLOMBIA']
            df = df[df['ESTU_DEPTO_RESIDE'].isin(COLOMBIA_DEPARTMENTS)]

        df = df.dropna(ignore_index=True)

        logger.info('( clean_dataframe ) Exporting')

        df.to_csv(os.path.join(self.DATA_DIR, f"""{
                  self.file_name}.csv"""), index=False)

    # + -------------------------------------------------------------------------------|>

    def add_departments(self) -> None:
        logger.info('( add_departments ) run')
        logger.info('( add_departments ) Adding the Departments')

        for department in COLOMBIA_DEPARTMENTS:
            Department.objects.get_or_create(name=department)

    # + -------------------------------------------------------------------------------|>

    def parse_municipalities(self, data: pd.DataFrame) -> None:
        logger.info('( parse_municipalities ) run')

        unlinked_municipalities = list(
            Municipality.objects.filter(department__isnull=True))
        if not unlinked_municipalities:
            logger.info('( parse_municipalities ) finished')
            return

        departments = {d.name: d for d in Department.objects.all()}
        unlinked_dict = {m.name: m for m in unlinked_municipalities}

        changes = []

        for _, row in data.iterrows():
            if not unlinked_dict:
                break

            if self.type == 'Saber11':
                department_name, municipality_name = row['COLE_DEPTO_UBICACION'], row['COLE_MCPIO_UBICACION']
                municipality = unlinked_dict.get(municipality_name)
                if municipality and municipality.department is None:
                    department = departments.get(department_name)
                    if department:
                        municipality.department = department
                        changes.append(municipality)
                        del unlinked_dict[municipality_name]

                continue

        if changes:
            with transaction.atomic():
                Municipality.objects.bulk_update(changes, ['department'])

        logger.info('( parse_municipalities ) finished')

    # + -------------------------------------------------------------------------------|>

    def parse_institutions(self, data: pd.DataFrame) -> None:
        logger.info('( parse_institutions ) run')

        def get_unlinked_institutions():
            if self.type == 'Saber11':
                return list(Highschool.objects.filter(municipality__isnull=True))

            if self.type == 'SaberPro':
                return list(College.objects.filter(municipality__isnull=True))

        unlinked_institutions = get_unlinked_institutions()
        if not unlinked_institutions:
            logger.info('( parse_institutions ) finished')
            return

        municipalities = {m.name: m for m in Municipality.objects.all()}
        unlinked_dict = {i.name: i for i in unlinked_institutions}

        changes = []

        for _, row in data.iterrows():
            if not unlinked_dict:
                break

            if self.type == 'Saber11':
                municipality_name, institution_name = row['COLE_MCPIO_UBICACION'], row['COLE_NOMBRE_ESTABLECIMIENTO']

                institution = unlinked_dict.get(institution_name)
                if institution and institution.municipality is None:
                    municipality = municipalities.get(municipality_name)
                    if municipality:
                        institution.municipality = municipality
                        changes.append(institution)
                        del unlinked_dict[institution_name]

                continue

        if changes:
            with transaction.atomic():
                if self.type == 'Saber11':
                    Highschool.objects.bulk_update(changes, ['municipality'])

                if self.type == 'SaberPro':
                    College.objects.bulk_update(changes, ['municipality'])

        logger.info(f'( parse_institutions ) finished')

    # + -------------------------------------------------------------------------------|>

    def parse_students(self, data: pd.DataFrame) -> None:
        logger.info('( parse_students ) run')

        if self.type == 'Saber11':
            logger.info('( parse_students ) removing previous students')

            Highschool.objects.all().delete()

            logger.info('( parse_students ) creating objects')

            highschools = {h.name: h for h in Highschool.objects.all()}

            students = [
                HighschoolStudent(
                    PUNT_ENGLISH=punt_english,
                    PUNT_MATHEMATICS=punt_math,
                    PUNT_SOCIAL_CITIZENSHIP=punt_social,
                    PUNT_NATURAL_SCIENCES=punt_natural,
                    PUNT_CRITICAL_READING=punt_languaje,
                    PUNT_GLOBAL=punt_global,
                    highschool=highschools.get(highschool_name),
                    period=period,
                    genre="MALE" if genre == "M" else "FEMALE"
                ) for punt_english, punt_math, punt_social, punt_natural, punt_languaje, punt_global, period, highschool_name, genre in data[[
                    'PUNT_INGLES', 'PUNT_MATEMATICAS', 'PUNT_SOCIALES_CIUDADANAS', 'PUNT_C_NATURALES', 'PUNT_LECTURA_CRITICA', 'PUNT_GLOBAL', 'PERIODO', 'COLE_NOMBRE_ESTABLECIMIENTO', 'ESTU_GENERO']].values]

            HighschoolStudent.objects.bulk_create(students)

            logger.info('( parse_students ) finished')

            return

    # ! -----------------------------------------------------------------------------------------------------|>

    def handle(self, *args: Any, **options: Any) -> None:
        logger.info('( handle ) Init')

        file_type: str = options['file_type']

        if not file_type in ['Saber11', 'SaberPro']:
            logger.fatal("( handle ) Invalid file type")
            return

        if file_type == 'Saber11':
            csv_file: str = os.path.join(self.DATA_DIR, "Resultados11.csv")
            self._type = 'Saber11'

        if file_type == 'SaberPro':
            csv_file: str = os.path.join(
                self.DATA_DIR, "ResultadosPro.csv")
            self._type = 'SaberPro'

        if not os.path.exists(csv_file):
            logger.fatal('( handle ) File not found')
            return

        logger.info('( handle ) File selected')

        self.clean_dataframe(file_path=csv_file)

        self.add_departments()

        logger.info('( handle ) Reading cleaned data')

        data = self.read_dataframe(file_path=os.path.join(
            self.DATA_DIR, f"{self.file_name}.csv"))

        self.fill(data=data)

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = [
                executor.submit(self.parse_municipalities, data),
                executor.submit(self.parse_institutions, data),
                # executor.submit(self.parse_students, data)
            ]

            for future in futures:
                future.result()

        logger.info('( handle ) Finished execution')
        os.remove(os.path.join(self.DATA_DIR, f"{self.file_name}.csv"))

    @property
    def type(self) -> Literal['Saber11', 'SaberPro']:
        return self._type

    @property
    def file_name(self) -> str:
        return self._file_name
