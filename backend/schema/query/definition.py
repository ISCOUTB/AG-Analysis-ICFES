import graphene
from saber.exceptions import DepartmentNotFoundError, MunicipalityNotFoundError, HighschoolNotFoundError, CollegeNotFoundError, PeriodNotFoundError
import schema.types as types
import saber.models as saber_models
from django.core.exceptions import ObjectDoesNotExist
from typing import Literal


class Query(graphene.ObjectType):
    # -----------------------------------------------------------------------------|>
    # Department
    # -----------------------------------------------------------------------------|>

    departments = graphene.List(types.DepartmentType)
    department = graphene.Field(types.DepartmentType, id=graphene.ID())

    def resolve_departments(self, info):
        return saber_models.Department.objects.all()

    def resolve_department(self, info, id):
        try:
            return saber_models.Department.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise DepartmentNotFoundError(id=str(id))

    # -----------------------------------------------------------------------------|>
    # Municipality
    # -----------------------------------------------------------------------------|>

    municipalities = graphene.List(
        types.MunicipalityType, department_id=graphene.ID(default_value=None))
    municipality = graphene.Field(types.MunicipalityType, id=graphene.ID())

    def resolve_municipalities(self, info, department_id=None):
        if department_id is None:
            return saber_models.Municipality.objects.all()
        try:
            department = saber_models.Department.objects.get(pk=department_id)
            return saber_models.Municipality.objects.filter(department=department)
        except ObjectDoesNotExist:
            raise DepartmentNotFoundError(id=str(department_id))

    def resolve_municipality(self, info, id):
        try:
            return saber_models.Municipality.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise MunicipalityNotFoundError(id=str(id))

    # -----------------------------------------------------------------------------|>
    # Highschool
    # -----------------------------------------------------------------------------|>

    highschools = graphene.List(
        types.HighschoolType, municipality_id=graphene.ID(default_value=None))
    highschool = graphene.Field(types.HighschoolType, id=graphene.ID())

    def resolve_highschools(self, info, municipality_id=None):
        if municipality_id is None:
            return saber_models.Highschool.objects.all()

        try:
            municipality = saber_models.Municipality.objects.get(
                pk=municipality_id)
            return saber_models.Highschool.objects.filter(municipality=municipality)
        except ObjectDoesNotExist:
            raise MunicipalityNotFoundError(id=str(municipality_id))

    def resolve_highschool(self, info, id):
        try:
            return saber_models.Highschool.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise HighschoolNotFoundError(id=str(id))

    # -----------------------------------------------------------------------------|>
    # College
    # -----------------------------------------------------------------------------|>

    colleges = graphene.List(
        types.CollegeType, municipality_id=graphene.ID(default_value=None))
    college = graphene.Field(types.CollegeType, id=graphene.ID())

    def resolve_colleges(self, info, municipality_id=None):
        if municipality_id is None:
            return saber_models.College.objects.all()

        try:
            municipality = saber_models.Municipality.objects.get(
                pk=municipality_id)
            return saber_models.College.objects.filter(municipality=municipality)
        except ObjectDoesNotExist:
            raise MunicipalityNotFoundError(id=str(municipality_id))

    def resolve_college(self, info, id):
        try:
            return saber_models.College.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise CollegeNotFoundError(id=str(id))

    # -----------------------------------------------------------------------------|>
    # Highschool Student
    # -----------------------------------------------------------------------------|>

    highschool_students = graphene.List(
        types.HighschoolStudentType,
        type=graphene.String(default_value="paginated"),
        period=graphene.String(default_value=None),
        start_period=graphene.String(default_value=None),
        end_period=graphene.String(default_value=None),
        page=graphene.Int(default_value=1),
        page_size=graphene.Int(default_value=1000)
    )

    def resolve_highschool_students(self, info, type: Literal['paginated', 'single_period', 'period_range'],
                                    period: str, start_period: str, end_period: str, page: int = 1, page_size: int = 1000):
        return Query.handler_students(
            qs=saber_models.HighschoolStudent.objects.all(),
            type=type,
            period=period,
            start_period=start_period,
            end_period=end_period,
            page=page,
            page_size=page_size
        )

    # -----------------------------------------------------------------------------|>
    # College Student
    # -----------------------------------------------------------------------------|>

    college_students = graphene.List(
        types.CollegeStudentType,
        type=graphene.String(default_value="paginated"),
        period=graphene.String(default_value=None),
        start_period=graphene.String(default_value=None),
        end_period=graphene.String(default_value=None),
        page=graphene.Int(default_value=1),
        page_size=graphene.Int(default_value=100)
    )

    def resolve_college_student(self, info, type: Literal['paginated', 'single_period', 'period_range'],
                                period: str, start_period: str, end_period: str, page: int = 1, page_size: int = 1000):

        return Query.handler_students(
            qs=saber_models.CollegeStudent.objects.all(),
            type=type,
            period=period,
            start_period=start_period,
            end_period=end_period,
            page=page,
            page_size=page_size
        )

    # -----------------------------------------------------------------------------|>
    # Periods
    # -----------------------------------------------------------------------------|>

    period = graphene.Field(types.PeriodType, id=graphene.ID())
    periods = graphene.List(
        types.PeriodType, type=graphene.String(default_value='Saber11'))

    def resolve_period(self, info, id):
        try:
            return saber_models.Period.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise PeriodNotFoundError(id=str(id))

    def resolve_periods(self, info, type: Literal['Saber11', 'SaberPro']):
        if type == 'Saber11':
            periods_id = saber_models.HighschoolStudent.objects.values_list(
                'period', flat=True).distinct()

            return saber_models.Period.objects.filter(id__in=periods_id)

        if type == 'SaberPro':
            periods_id = saber_models.CollegeStudent.objects.values_list(
                'period', flat=True).distinct()

            return saber_models.Period.objects.filter(id__in=periods_id)

        return saber_models.Period.objects.all()

    # -----------------------------------------------------------------------------|>
    # Misc
    # -----------------------------------------------------------------------------|>

    @staticmethod
    def handler_students(qs: list[saber_models.CollegeStudent | saber_models.HighschoolStudent],
                         type: Literal['paginated', 'single_period', 'period_range'], period: str, start_period: str, end_period: str,
                         page: int, page_size: int):
        if type == 'paginated':
            start = (page - 1) * page_size
            end = start + page_size

            return qs[start:end]

        if type == 'single_period':
            if not period:
                raise Exception(':period is required')

            try:
                period_object = saber_models.Period.objects.get(label=period)
                return qs.filter(period=period_object)
            except ObjectDoesNotExist:
                return []

        if type == 'period_range':
            if not start_period or not end_period:
                raise Exception(':start_period, :end_period are required')

            try:
                periods = saber_models.Period.objects.filter(
                    label__gte=start_period,
                    label__lte=end_period
                )

                if not periods.exists():
                    return []

                qs = qs.filter(period__in=periods)
                start = (page - 1) * page_size
                end = start + page_size
                return qs[start:end]
            except:
                return []
        return []
