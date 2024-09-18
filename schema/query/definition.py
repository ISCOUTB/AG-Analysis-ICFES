import graphene
from saber.exceptions import DepartmentNotFoundError, MunicipalityNotFoundError, HighschoolNotFoundError, CollegeNotFoundError, StudentsReportsNotFound
import schema.types as types
import saber.models as saber_models
from django.core.exceptions import ObjectDoesNotExist


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

    municipalities = graphene.List(types.MunicipalityType)
    municipality = graphene.Field(types.MunicipalityType, id=graphene.ID())

    def resolve_municipalities(self, info):
        return saber_models.Municipality.objects.all()

    def resolve_municipality(self, info, id):
        try:
            return saber_models.Municipality.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise MunicipalityNotFoundError(id=str(id))

    # -----------------------------------------------------------------------------|>
    # Highschool
    # -----------------------------------------------------------------------------|>

    highschools = graphene.List(types.HighschoolType)
    highschool = graphene.Field(types.HighschoolType, id=graphene.ID())

    def resolve_highschools(self, info):
        return saber_models.Highschool.objects.all()

    def resolve_highschool(self, info, id):
        try:
            return saber_models.Highschool.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise HighschoolNotFoundError(id=str(id))

    # -----------------------------------------------------------------------------|>
    # College
    # -----------------------------------------------------------------------------|>

    colleges = graphene.List(types.CollegeType)
    college = graphene.Field(types.CollegeType, id=graphene.ID())

    def resolve_colleges(self, info):
        return saber_models.College.objects.all()

    def resolve_college(self, info, id):
        try:
            return saber_models.College.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise CollegeNotFoundError(id=str(id))

    # -----------------------------------------------------------------------------|>
    # Highschool Student
    # -----------------------------------------------------------------------------|>

    highschool_students = graphene.List(types.HighschoolStudentType)

    def resolve_highschool_students(self, info):
        return saber_models.HighschoolStudent.objects.all()

    # -----------------------------------------------------------------------------|>
    # College Student
    # -----------------------------------------------------------------------------|>

    college_students = graphene.List(types.CollegeStudentType)

    def resolve_college_student(self, info):
        return saber_models.CollegeStudent.objects.all()
