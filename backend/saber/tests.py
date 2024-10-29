from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Department, Municipality, Highschool, College
from .serializers import DepartmentSerializer, MunicipalitySerializer, HighschoolSerializer, CollegeSerializer


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
