from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Department, Municipality, Highschool, College, HighschoolStudent, CollegeStudent, Period
from .serializers import DepartmentSerializer, MunicipalitySerializer, HighschoolSerializer, CollegeSerializer, HighschoolStudentSerializer, CollegeStudentSerializer
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    # GET /:id/municipalities
    @action(detail=True, methods=['GET'])
    def municipalities(self, request, pk=None):
        try:
            department = Department.objects.get(pk=pk)

            municipalities = Municipality.objects.filter(department=department)

            serializer = MunicipalitySerializer(municipalities, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'department with the given :pk does not exists'}, status=status.HTTP_400_BAD_REQUEST)


class MunicipalityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer

    # GET /:id/highschools
    @action(detail=True, methods=['GET'])
    def highschools(self, request, pk=None):
        try:
            municipality = Municipality.objects.get(pk=pk)

            highschools = Highschool.objects.filter(municipality=municipality)

            serializer = HighschoolSerializer(highschools, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'municipality with the given :pk does not exists'}, status=status.HTTP_400_BAD_REQUEST)

    # GET /:id/colleges
    @action(detail=True, methods=['GET'])
    def colleges(self, request, pk=None):
        try:
            municipality = Municipality.objects.get(pk=pk)

            colleges = College.objects.filter(municipality=municipality)

            serializer = CollegeSerializer(colleges, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'municipality with the given :pk does not exists'}, status=status.HTTP_400_BAD_REQUEST)


class HighschoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Highschool.objects.all()
    serializer_class = HighschoolSerializer

    # POST /students
    @action(detail=False, methods=['POST'])
    def students(self, request):
        body = request.data

        queryset = HighschoolStudent.objects.all()
        deparment_id = body.get('department')
        municipality_id = body.get('municipality')
        highschool_id = body.get('highschool')
        period_id = body.get('period')

        if deparment_id:
            try:
                queryset = queryset.filter(
                    highschool__municipality__department_id=deparment_id
                )
            except ObjectDoesNotExist:
                return Response({'detail': 'department with the given :pk does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if municipality_id:
            try:
                queryset = queryset.filter(
                    highschool_municipality_id=municipality_id)
            except ObjectDoesNotExist:
                return Response({'detail': 'municipality with the given :pk does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if highschool_id:
            try:
                highschool = Highschool.objects.get(pk=highschool_id)
                queryset = queryset.filter(highschool=highschool)
            except ObjectDoesNotExist:
                return Response({'detail': 'highschool with the given :pk does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if period_id:
            try:
                period = Period.objects.get(pk=period_id)
                queryset = queryset.filter(period=period)
            except ObjectDoesNotExist:
                return Response({'detail': 'period with the given :pk does not exists'})

        page = body.get('page', 1)
        page_size = body.get('pageSize', 1000)

        start = (page - 1) * page_size
        end = start + page_size

        serializer = HighschoolStudentSerializer(
            queryset[start:end], many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # GET /:id/students_count
    @action(detail=True, methods=['GET'])
    def students_count(self, request, pk=None):
        try:
            highschool = Highschool.objects.get(pk=pk)

            students = HighschoolStudent.objects.filter(highschool=highschool)

            return Response({'count': len(students)}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'highschool with the given :pk does not exists'}, status=status.HTTP_400_BAD_REQUEST)


class CollegeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

    # POST /students
    @action(detail=False, methods=['POST'])
    def students(self, request, pk=None):
        body = request.data

        queryset = CollegeStudent.objects.all()
        deparment_id = body.get('department')
        municipality_id = body.get('municipality')
        college_id = body.get('college')
        period_id = body.get('period')

        if deparment_id:
            try:
                queryset = queryset.filter(
                    college__municipality__department_id=deparment_id
                )
            except ObjectDoesNotExist:
                return Response({'detail': 'department with the given :pk does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if municipality_id:
            try:
                queryset = queryset.filter(
                    college_municipality_id=municipality_id)
            except ObjectDoesNotExist:
                return Response({'detail': 'municipality with the given :pk does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if college_id:
            try:
                college = College.objects.get(pk=college_id)
                queryset = queryset.filter(college=college)
            except ObjectDoesNotExist:
                return Response({'detail': 'college with the given :pk does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        if period_id:
            try:
                period = Period.objects.get(pk=period_id)
                queryset = queryset.filter(period=period)
            except ObjectDoesNotExist:
                return Response({'detail': 'period with the given :pk does not exists'})

        page = body.get('page', 1)
        page_size = body.get('pageSize', 1000)

        start = (page - 1) * page_size
        end = start + page_size

        serializer = CollegeStudentSerializer(
            queryset[start:end], many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

     # GET /:id/students_count
    @action(detail=True, methods=['GET'])
    def students_count(self, request, pk=None):
        try:
            college = College.objects.get(pk=pk)

            students = CollegeStudent.objects.filter(college=college)

            return Response({'count': len(students)}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'college with the given :pk does not exists'}, status=status.HTTP_400_BAD_REQUEST)
