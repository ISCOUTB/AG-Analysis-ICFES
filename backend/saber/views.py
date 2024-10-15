from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Department, Municipality, Highschool, College, HighschoolStudent, CollegeStudent, Period
from .serializers import DepartmentSerializer, MunicipalitySerializer, HighschoolSerializer, CollegeSerializer, HighschoolStudentSerializer, CollegeStudentSerializer, PeriodSerializer
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from rest_framework import status


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def list(self, request):
        name = request.query_params.get('name')

        if name:
            department = get_object_or_404(Department, name__iexact=name)
            serializer = self.get_serializer(department)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().list(request)

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

    def list(self, request):
        name = request.query_params.get('name')

        if name:
            municipality = get_object_or_404(Municipality, name__iexact=name)
            serializer = self.get_serializer(municipality)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().list(request)

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

    def list(self, request):
        name = request.query_params.get('name')

        if name:
            highschool = get_object_or_404(Highschool, name__iexact=name)
            serializer = self.get_serializer(highschool)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().list(request)

    # POST /students_paginated
    @action(detail=False, methods=['POST'])
    def students_paginated(self, request):
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
                    highschool__municipality_id=municipality_id)
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

    # POST /students_stream
    @action(detail=False, methods=['POST'])
    def students_stream(self, request):
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
                    highschool__municipality_id=municipality_id)
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

        page_size = body.get('pageSize', 1000)
        total_items = queryset.count()

        def event_stream():
            for start in range(0, total_items, page_size):
                end = start + page_size

                page_data = queryset[start:end]

                serializer = HighschoolStudentSerializer(page_data, many=True)

                yield serializer.data

        response = StreamingHttpResponse(
            event_stream(), content_type='text/event-stream'
        )

        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

    # POST /students_count
    @action(detail=False, methods=['POST'])
    def students_count(self, request, pk=None):
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
                    highschool__municipality_id=municipality_id)
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

        return Response({'count': len(queryset)}, status=status.HTTP_200_OK)

    # GET /periods
    @action(detail=False, methods=['GET'])
    def periods(self, request):
        periods_id = HighschoolStudent.objects.values_list(
            'period', flat=True).distinct()

        periods = Period.objects.filter(id__in=periods_id)

        serializer = PeriodSerializer(periods, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CollegeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

    def list(self, request):
        name = request.query_params.get('name')

        if name:
            college = get_object_or_404(College, name__iexact=name)
            serializer = self.get_serializer(college)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().list(request)

    # POST /students_paginated
    @action(detail=False, methods=['POST'])
    def students_paginated(self, request, pk=None):
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
                    college__municipality_id=municipality_id)
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

    # POST /students_stream
    @action(detail=False, methods=['POST'])
    def students_stream(self, request, pk=None):
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
                    college__municipality_id=municipality_id)
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

        page_size = body.get('pageSize', 1000)
        total_items = queryset.count()

        def event_stream():
            for start in range(0, total_items, page_size):
                end = start + page_size

                page_data = queryset[start:end]

                serializer = CollegeStudentSerializer(page_data, many=True)

                yield serializer.data

        response = StreamingHttpResponse(
            event_stream(), content_type='text/event-stream'
        )

        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

     # POST /students_count
    @action(detail=False, methods=['POST'])
    def students_count(self, request, pk=None):
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
                    college__municipality_id=municipality_id)
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

        return Response({'count': len(queryset)}, status=status.HTTP_200_OK)

    # GET /periods
    @action(detail=False, methods=['GET'])
    def periods(self, request):
        periods_id = CollegeStudent.objects.values_list(
            'period', flat=True).distinct()

        periods = Period.objects.filter(id__in=periods_id)

        serializer = PeriodSerializer(periods, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PeriodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer

    def list(self, request):
        label = request.query_params.get('label')

        if label:
            period = get_object_or_404(Period, label__iexact=label)
            serializer = self.get_serializer(period)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().list(request)
