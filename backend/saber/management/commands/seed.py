from typing import Literal, Any
from django.core.management.base import BaseCommand, CommandParser
from data.constants import COLOMBIA_DEPARTMENTS
from django.conf import settings
from django.db import transaction
from saber.models import Department, Municipality, Highschool, HighschoolStudent, College, CollegeStudent, Period
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
            def fill_municipalities_saber11() -> None:
                logger.info('( fill_municipalities ) run')

                for name in data['COLE_MCPIO_UBICACION'].unique():
                    Municipality.objects.get_or_create(name=name)

            def fill_highschools_saber11() -> None:
                logger.info('( fill_highschools ) run')

                for name in data['COLE_NOMBRE_ESTABLECIMIENTO'].unique():
                    Highschool.objects.get_or_create(name=name)

            def fill_periods_saber11() -> None:
                logger.info('( fill_periods ) run')

                for label in data['PERIODO'].unique():
                    Period.objects.get_or_create(label=label)

            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                futures = [
                    executor.submit(fill_municipalities_saber11),
                    executor.submit(fill_highschools_saber11),
                    executor.submit(fill_periods_saber11)
                ]

                for future in futures:
                    future.result()

            return

        if self.type == 'SaberPro':
            def fill_municipalities_saberpro() -> None:
                logger.info('( fill_municipalities ) run')

                for name in data['ESTU_INST_MUNICIPIO'].unique():
                    Municipality.objects.get_or_create(name=name)

            def fill_colleges_saberpro() -> None:
                logger.info('( fill_colleges ) run')

                for name in data['INST_NOMBRE_INSTITUCION'].unique():
                    College.objects.get_or_create(name=name)

            def fill_periods_saberpro() -> None:
                logger.info('( fill_periods ) run')

                for label in data['PERIODO'].unique():
                    Period.objects.get_or_create(label=label)

            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                futures = [
                    executor.submit(fill_municipalities_saberpro),
                    executor.submit(fill_colleges_saberpro),
                    executor.submit(fill_periods_saberpro)
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

            if self.type == 'SaberPro':
                department_name, municipality_name = row['ESTU_INST_DEPARTAMENTO'], row['ESTU_INST_MUNICIPIO']
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

            if self.type == 'SaberPro':
                municipality_name, institution_name = row['ESTU_INST_MUNICIPIO'], row['INST_NOMBRE_INSTITUCION']

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
            with transaction.atomic():
                logger.info('( parse_students ) removing previous students')
                HighschoolStudent.objects.all().delete()

                logger.info('( parse_students ) creating objects')
                highschools = {h.name: h for h in Highschool.objects.all()}
                periods = {p.label: p for p in Period.objects.all()}

                def process_chunk_saber11(chunk: pd.DataFrame) -> None:
                    students = [
                        HighschoolStudent(
                            PUNT_ENGLISH=row['PUNT_INGLES'],
                            PUNT_MATHEMATICS=row['PUNT_MATEMATICAS'],
                            PUNT_SOCIAL_CITIZENSHIP=row['PUNT_SOCIALES_CIUDADANAS'],
                            PUNT_NATURAL_SCIENCES=row['PUNT_C_NATURALES'],
                            PUNT_CRITICAL_READING=row['PUNT_LECTURA_CRITICA'],
                            PUNT_GLOBAL=row['PUNT_GLOBAL'],
                            highschool=highschools.get(
                                row['COLE_NOMBRE_ESTABLECIMIENTO']),
                            period=periods.get(row['PERIODO']),
                            genre="MALE" if row['ESTU_GENERO'] == "M" else "FEMALE"
                        ) for _, row in chunk.iterrows()
                    ]

                    HighschoolStudent.objects.bulk_create(students)

                num_chunks: int = os.cpu_count()
                chunk_size: int = 10000
                chunks: list[pd.DataFrame] = [data.iloc[i:i + chunk_size]
                                              for i in range(0, len(data), chunk_size)]

                logger.info('( parse_students ) creating threads')

                with ThreadPoolExecutor(max_workers=num_chunks) as executor:
                    logger.info('( parse_students ) running threads')

                    futures = [executor.submit(process_chunk_saber11, chunk)
                               for chunk in chunks]
                    for future in futures:
                        future.result()

                logger.info('( parse_students ) finished')

            return

        if self.type == 'SaberPro':
            with transaction.atomic():
                logger.info('( parse_students ) removing previous students')
                CollegeStudent.objects.all().delete()

                logger.info('( parse_students ) creating objects')
                colleges = {c.name: c for c in College.objects.all()}
                periods = {p.label: p for p in Period.objects.all()}

                def process_chunk_saberpro(chunk: pd.DataFrame) -> None:
                    students = [
                        CollegeStudent(
                            MOD_QUANTITATIVE_REASONING=row['MOD_RAZONA_CUANTITAT_PUNT'],
                            MOD_WRITTEN_COMMUNICATION=row['MOD_COMUNI_ESCRITA_PUNT'],
                            MOD_CRITICAL_READING=row['MOD_LECTURA_CRITICA_PUNT'],
                            MOD_ENGLISH=row['MOD_INGLES_PUNT'],
                            MOD_CITIZENSHIP_COMPETENCES=row['MOD_COMPETEN_CIUDADA_PUNT'],
                            college=colleges.get(
                                row['INST_NOMBRE_INSTITUCION']),
                            period=periods.get(row['PERIODO']),
                            genre="MALE" if row['ESTU_GENERO'] == "M" else "FEMALE"
                        ) for _, row in chunk.iterrows()
                    ]

                    CollegeStudent.objects.bulk_create(students)

                num_chunks: int = os.cpu_count()
                chunk_size: int = 10000
                chunks: list[pd.DataFrame] = [data.iloc[i:i + chunk_size]
                                              for i in range(0, len(data), chunk_size)]

                logger.info('( parse_students ) creating threads')

                with ThreadPoolExecutor(max_workers=num_chunks) as executor:
                    logger.info('( parse_students ) running threads')

                    futures = [executor.submit(process_chunk_saberpro, chunk)
                               for chunk in chunks]
                    for future in futures:
                        future.result()

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
            ]

            for future in futures:
                future.result()

        self.parse_students(data=data)

        os.remove(os.path.join(self.DATA_DIR, f"{self.file_name}.csv"))
        logger.info('( handle ) Finished execution')

    @property
    def type(self) -> Literal['Saber11', 'SaberPro']:
        return self._type

    @property
    def file_name(self) -> str:
        return self._file_name
