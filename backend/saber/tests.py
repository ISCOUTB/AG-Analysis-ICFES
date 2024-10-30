from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Department, Municipality, Highschool, College, HighschoolStudent, CollegeStudent, Period, GENRE
from .serializers import DepartmentSerializer, MunicipalitySerializer, HighschoolSerializer, CollegeSerializer, HighschoolStudentSerializer, CollegeStudentSerializer
import random


class DepartmentTestCase(APITestCase):
    def setUp(self) -> None:
        # Initial Setup

        self.department = Department.objects.create(name='Department Name 1')
        self.list_url = reverse('department-list')
        self.detail_url = reverse(
            'department-detail', args=[self.department.id])

        # GET /:id/municipalities

        for i in range(10):
            Municipality.objects.create(
                name=f'Name {i}', department=self.department)

        self.municipalities_url = reverse(
            'department-municipalities', args=[self.department.id])

    def test_list_department(self):
        response = self.client.get(self.list_url)
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_department(self):
        response = self.client.get(self.detail_url)
        department = Department.objects.get(id=self.department.id)
        serializer = DepartmentSerializer(department)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_municipalities(self):
        response = self.client.get(self.municipalities_url)
        municipalities = Municipality.objects.all()
        serializer = MunicipalitySerializer(municipalities, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class MunicipalityTestCase(APITestCase):
    def setUp(self) -> None:
        # Initial Setup

        self.department = Department.objects.create(name='Department Name')
        self.municipality = Municipality.objects.create(
            name='Municipality Name')
        self.no_objects = 10

        self.list_url = reverse('municipality-list')
        self.detail_url = reverse(
            'municipality-detail', args=[self.municipality.id])

        # GET /:id/highschools

        for i in range(self.no_objects):
            Highschool.objects.create(
                name=f'Highschool {i}', municipality=self.municipality)

        self.highschools_url = reverse(
            'municipality-highschools', args=[self.municipality.id])

        # GET /:id/colleges

        for i in range(self.no_objects):
            College.objects.create(
                name=f'College {i}', municipality=self.municipality)

        self.college_url = reverse(
            'municipality-colleges', args=[self.municipality.id])

    def test_list_municipality(self):
        response = self.client.get(self.list_url)
        municipalities = Municipality.objects.all()
        serializer = MunicipalitySerializer(municipalities, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_municipality(self):
        response = self.client.get(self.detail_url)
        municipality = Municipality.objects.get(id=self.municipality.id)
        serializer = MunicipalitySerializer(municipality)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_highschools(self):
        response = self.client.get(self.highschools_url)
        highschools = Highschool.objects.all()
        serializer = HighschoolSerializer(highschools, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_colleges(self):
        response = self.client.get(self.college_url)
        colleges = College.objects.all()
        serializer = CollegeSerializer(colleges, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class HighschoolTestCase(APITestCase):
    def setUp(self) -> None:
        department = Department.objects.create(name='Department Name 1')
        self.municipality = Municipality.objects.create(
            name='Municipality Name 1', department=department)
        self.highschool = Highschool.objects.create(
            name='Highschool Name 1', municipality=self.municipality)

        self.list_url = reverse('highschool-list')
        self.detail_url = reverse(
            'highschool-detail', args=[self.highschool.id])

        # POST /students_paginated

        period = Period.objects.create(label='1234')

        for i in range(100):
            HighschoolStudent.objects.create(
                PUNT_ENGLISH=random.randint(0, 100),
                PUNT_MATHEMATICS=random.randint(0, 100),
                PUNT_SOCIAL_CITIZENSHIP=random.randint(0, 100),
                PUNT_NATURAL_SCIENCES=random.randint(0, 100),
                PUNT_CRITICAL_READING=random.randint(0, 100),
                PUNT_GLOBAL=random.randint(0, 100),
                highschool=self.highschool,
                genre=random.choice(GENRE),
                period=period
            )

        self.students_paginated_url = reverse('highschool-students-paginated')

    def test_list_highschool(self):
        response = self.client.get(self.list_url)
        highschools = Highschool.objects.all()
        serializer = HighschoolSerializer(highschools, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_highschool(self):
        response = self.client.get(self.detail_url)
        highschool = Highschool.objects.get(id=self.highschool.id)
        serializer = HighschoolSerializer(highschool)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_students_paginated(self):
        response = self.client.post(self.students_paginated_url)
        highschool_students = HighschoolStudent.objects.all()
        serializer = HighschoolStudentSerializer(
            highschool_students, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class CollegeTestCase(APITestCase):
    def setUp(self) -> None:
        department = Department.objects.create(name='Department Name 1')
        self.municipality = Municipality.objects.create(
            name='Municipality Name 1', department=department)
        self.college = College.objects.create(
            name='College Name 1', municipality=self.municipality)

        self.list_url = reverse('college-list')
        self.detail_url = reverse(
            'college-detail', args=[self.college.id])

        # POST /students_paginated

        period = Period.objects.create(label='1234')

        for i in range(100):
            CollegeStudent.objects.create(
                MOD_QUANTITATIVE_REASONING=random.randint(0, 100),
                MOD_WRITTEN_COMMUNICATION=random.randint(0, 100),
                MOD_CRITICAL_READING=random.randint(0, 100),
                MOD_ENGLISH=random.randint(0, 100),
                MOD_CITIZENSHIP_COMPETENCES=random.randint(0, 100),
                college=self.college,
                genre=random.choice(GENRE),
                period=period
            )

        self.students_paginated_url = reverse('college-students-paginated')

    def test_list_college(self):
        response = self.client.get(self.list_url)
        colleges = College.objects.all()
        serializer = HighschoolSerializer(colleges, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_highschool(self):
        response = self.client.get(self.detail_url)
        college = College.objects.get(id=self.college.id)
        serializer = CollegeSerializer(college)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_students_paginated(self):
        response = self.client.post(self.students_paginated_url)
        college_students = CollegeStudent.objects.all()
        serializer = CollegeStudentSerializer(
            college_students, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
