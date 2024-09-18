from django.db import models

MALE = "MALE"
FEMALE = "FEMALE"
OTHER = "OTHER"

GENRE = [
    (MALE, MALE),
    (FEMALE, FEMALE),
    (OTHER, OTHER)
]


class BaseInstitution(models.Model):
    name = models.TextField()

    class Meta:
        abstract = True


class BaseStudent(models.Model):
    genre = models.CharField(max_length=20, choices=GENRE)

    class Meta:
        abstract = True


class HighschoolStudent(BaseStudent):
    highschool = models.ForeignKey(
        'Highschool', on_delete=models.CASCADE, related_name='highschool_students')
    PUNT_ENGLISH = models.FloatField()
    PUNT_MATHEMATICS = models.FloatField()
    PUNT_SOCIAL_CITIZENSHIP = models.FloatField()
    PUNT_NATURAL_SCIENCES = models.FloatField()
    PUNT_CRITICAL_READING = models.FloatField()
    PUNT_GLOBAL = models.FloatField()


class Highschool(BaseInstitution):
    municipality = models.ForeignKey(
        'Municipality', on_delete=models.CASCADE, related_name='highschools')


class CollegeStudent(BaseStudent):
    college = models.ForeignKey(
        'College', on_delete=models.CASCADE, related_name='college_students')
    MOD_QUANTITATIVE_REASONING = models.FloatField()
    MOD_WRITTEN_COMMUNICATION = models.FloatField()
    MOD_CRITICAL_READING = models.FloatField()
    MOD_ENGLISH = models.FloatField()
    MOD_CITIZENSHIP_COMPETENCES = models.FloatField()


class College(BaseInstitution):
    municipality = models.ForeignKey(
        'Municipality', on_delete=models.CASCADE, related_name='colleges')


class Municipality(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, related_name='municipalities')


class Department(models.Model):
    name = models.CharField(max_length=255)
