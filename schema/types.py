from graphene_django import DjangoObjectType
import saber.models as saber_models
import graphene


class DepartmentType(DjangoObjectType):
    class Meta:
        model = saber_models.Department


class MunicipalityType(DjangoObjectType):
    class Meta:
        model = saber_models.Municipality


class HighschoolStudentType(DjangoObjectType):

    class Meta:
        model = saber_models.HighschoolStudent


class CollegeStudentType(DjangoObjectType):
    class Meta:
        model = saber_models.CollegeStudent


class CollegeType(DjangoObjectType):
    students = graphene.List(CollegeStudentType)

    class Meta:
        model = saber_models.College

    def resolve_students(self, info):
        return self.college_students.all()


class HighschoolType(DjangoObjectType):
    students = graphene.List(HighschoolStudentType)

    class Meta:
        model = saber_models.Highschool

    def resolve_students(self, info):
        return self.highschool_students.all()
