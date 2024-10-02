from typing import Any, Literal, Dict
from django.core.management.base import BaseCommand, CommandParser
from saber.models import Department, Municipality, Highschool, College, HighschoolStudent, CollegeStudent, Period
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor
import logging
import numpy as np
import sys
import json
import os

logger = logging.getLogger('saber')


class Command(BaseCommand):
    DATA_DIR: str = os.path.join(settings.BASE_DIR, "data")

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '-T', '--type', choices=['places', 'students', 'periods'], help='Type of JSON to be generated')

        parser.add_argument('-St', '--student-type', choices=[
                            'Saber11', 'SaberPro'], help='Type of students to be generated', nargs='?')

    def export(self, json_object, file_name: str) -> None:
        with open(os.path.join(
                self.DATA_DIR, file_name), "w", encoding='utf-8') as output_file:
            json.dump(json_object, output_file)

    # ! -----------------------------------------------------------------------------------------------------|>

    def handle_places(self) -> None:
        logger.info('( handle_places ) run')

        logger.info('( handle_places ) creating objects')

        departments = {d.name: d for d in Department.objects.all()}
        municipalities = {m.name: m for m in Municipality.objects.all()}
        highschools = {h.name: h for h in Highschool.objects.all()}
        colleges = {c.name: c for c in College.objects.all()}

        json_object = {}

        logger.info('( handle_places ) iterating')
        for department_name, department in departments.items():
            json_object[department_name] = {}

            for municipality_name, municipality in municipalities.items():
                if municipality.department == department:
                    json_object[department_name][municipality_name] = {
                        'highschools': [],
                        'colleges': []
                    }

                    for highschool_name, highschool in highschools.items():
                        if highschool.municipality == municipality:
                            json_object[department_name][municipality_name]['highschools'].append(
                                {'name': highschool_name, 'id': highschool.pk})

                    for college_name, college in colleges.items():
                        if college.municipality == municipality:
                            json_object[department_name][municipality_name]['colleges'].append(
                                {'name': college_name, 'id': college.pk})

        logger.info('( handle_places ) exporting ')
        self.export(json_object=json_object, file_name='places.json')

    # + -------------------------------------------------------------------------------|>

    def handle_students(self, type: Literal['Saber11', 'SaberPro']) -> None:
        logger.info('( handle_students ) run')

        if type == 'Saber11':
            schools = {h.name: h for h in Highschool.objects.all()}

            os.makedirs(os.path.join(self.DATA_DIR, type), exist_ok=True)

            def process_chunk_saber11(chunk: Dict[Any, Highschool], chunk_index: int) -> None:
                json_object = {}

                for institution in chunk.values():
                    json_object[institution.name] = []

                    for student in HighschoolStudent.objects.filter(highschool=institution):
                        json_object[institution.name].append({
                            'data': {
                                'PUNT_ENGLISH': student.PUNT_ENGLISH,
                                'PUNT_MATHEMATICS': student.PUNT_MATHEMATICS,
                                'PUNT_SOCIAL_CITIZENSHIP': student.PUNT_SOCIAL_CITIZENSHIP,
                                'PUNT_NATURAL_SCIENCES': student.PUNT_NATURAL_SCIENCES,
                                'PUNT_CRITICAL_READING': student.PUNT_CRITICAL_READING,
                                'PUNT_GLOBAL': student.PUNT_GLOBAL,
                            },
                            'highschool_id': institution.pk
                        })

                self.export(json_object=json_object, file_name=os.path.join(
                    type, f'{type}_{chunk_index}.json'))

            num_workers: int | None = os.cpu_count()
            chunks = np.array_split(
                list(schools.items()), np.ceil(len(schools) / num_workers * 8))

            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = [
                    executor.submit(process_chunk_saber11, dict(chunk_tuple), i) for i, chunk_tuple in enumerate(chunks)
                ]

                for future in futures:
                    future.result()

            return

        if type == 'SaberPro':
            schools = {h.name: h for h in College.objects.all()}

            os.makedirs(os.path.join(self.DATA_DIR, type), exist_ok=True)

            def process_chunk_saber11(chunk: Dict[Any, College], chunk_index: int) -> None:
                json_object = {}

                for institution in chunk.values():
                    json_object[institution.name] = []

                    for student in CollegeStudent.objects.filter(college=institution):
                        json_object[institution.name].append({
                            'data': {
                                'MOD_CITIZENSHIP_COMPETENCES': student.MOD_CITIZENSHIP_COMPETENCES,
                                'MOD_CRITICAL_READING': student.MOD_CRITICAL_READING,
                                'MOD_ENGLISH': student.MOD_ENGLISH,
                                'MOD_QUANTITATIVE_REASONING': student.MOD_QUANTITATIVE_REASONING,
                                'MOD_WRITTEN_COMMUNICATION': student.MOD_WRITTEN_COMMUNICATION,
                            },
                            'college_id': institution.pk
                        })

                self.export(json_object=json_object, file_name=os.path.join(
                    type, f'{type}_{chunk_index}.json'))

            num_workers: int | None = os.cpu_count()
            chunks = np.array_split(
                list(schools.items()), np.ceil(len(schools) / num_workers * 4))

            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = [
                    executor.submit(process_chunk_saber11, dict(chunk_tuple), i) for i, chunk_tuple in enumerate(chunks)
                ]

                for future in futures:
                    future.result()

            return

    # + -------------------------------------------------------------------------------|>

    def handle_periods(self) -> None:
        logger.info('( handle_periods ) run')
        logger.info('( handle_periods ) creating objects ')
        json_object = {p.pk: p.label for p in Period.objects.all()}

        logger.info('( handle_periods ) exporting')
        self.export(json_object=json_object, file_name='periods.json')

    # ! -----------------------------------------------------------------------------------------------------|>

    def handle(self, *args: Any, **options: Any) -> None:
        logger.info('( handle ) init ')

        json_type: Literal['places', 'students', 'periods'] = options['type']
        student_type: Literal['Saber11',
                              'SaberPro'] | None = options['student_type']

        if json_type == 'students' and student_type is None:
            logger.fatal('( handle ) :student_type param is [ Required ]')
            sys.exit(0)

        if json_type == 'places':
            self.handle_places()

        if json_type == 'students':
            self.handle_students(type=student_type)

        if json_type == 'periods':
            self.handle_periods()

        logger.info('( handle ) finished')
