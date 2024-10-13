from rest_framework import serializers
from .models import Department, Municipality, Highschool, College, HighschoolStudent, CollegeStudent


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = "__all__"


class HighschoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highschool
        fields = "__all__"


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"


class HighschoolStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighschoolStudent
        fields = "__all__"


class CollegeStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeStudent
        fields = "__all__"
