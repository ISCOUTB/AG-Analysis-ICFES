from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Department
from .serializers import DepartmentSerializer


class DepartmentTestCase(APITestCase):
    def setUp(self) -> None:
        self.department = Department.objects.create(name='Department Name 1')
        self.list_url = reverse('department-list')
        self.detail_url = reverse(
            'department-detail', args=[self.department.id])

    def test_list_books(self):
        response = self.client.get(self.list_url)
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        department = Department.objects.get(id=self.department.id)
        serializer = DepartmentSerializer(department)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
