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

    def process_students(self, school_model: Highschool | College,
                         student_model: HighschoolStudent | CollegeStudent,
                         type: Literal['Saber11', 'SaberPro'], data_fields: list[str]) -> None:
        logger.info('( process_students ) run')

        logger.info('( process_students ) creating objects')
        students = {s.pk: s for s in student_model.objects.all()}

        os.makedirs(os.path.join(self.DATA_DIR, "students"), exist_ok=True)

        logger.info('( process_students ) iterating ')

        def process_chunk(chunk: Dict[Any, HighschoolStudent | CollegeStudent], chunk_index: int):
            chunk_data = {}
             
            self.export(json_object=chunk_data, file_name=os.path.join(
                'students', f'{type}_{chunk_index}.json'))

        num_chunks: int = os.cpu_count()
        chunk_size: int = 10000
        chunks = np.array_split(list(students.items()),
                                np.ceil(len(students) / chunk_size))

        with ThreadPoolExecutor(max_workers=num_chunks) as executor:
            futures = [
                executor.submit(process_chunk, dict(chunk), i) for i, chunk in enumerate(chunks)
            ]
            for future in futures:
                future.result()

    def handle_students(self, type: Literal['Saber11', 'SaberPro']) -> None:
        logger.info('( handle_students ) run')

        if type == 'Saber11':
            self.process_students(school_model=Highschool, student_model=HighschoolStudent, type='Saber11', data_fields=[
                                  'PUNT_CRITICAL_READING', 'PUNT_ENGLISH', 'PUNT_GLOBAL', 'PUNT_MATHEMATICS', 'PUNT_NATURAL_SCIENCES', 'PUNT_SOCIAL_CITIZENSHIP'])

            return

        if type == 'SaberPro':
            self.process_students(school_model=College, student_model=CollegeStudent, type='SaberPro', data_fields=[
                'MOD_CITIZENSHIP_COMPETENCES', 'MOD_CRITICAL_READING', 'MOD_ENGLISH', 'MOD_WRITTEN_COMMUNICATION', 'MOD_QUANTITATIVE_REASONING'])

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
