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
    period = models.CharField(max_length=10)

    class Meta:
        abstract = True


class HighschoolStudent(BaseStudent):
    highschool = models.ForeignKey(
        'Highschool', on_delete=models.CASCADE, related_name='highschool_students')
    PUNT_ENGLISH = models.IntegerField()
    PUNT_MATHEMATICS = models.IntegerField()
    PUNT_SOCIAL_CITIZENSHIP = models.IntegerField()
    PUNT_NATURAL_SCIENCES = models.IntegerField()
    PUNT_CRITICAL_READING = models.IntegerField()
    PUNT_GLOBAL = models.IntegerField()


class Highschool(BaseInstitution):
    municipality = models.ForeignKey(
        'Municipality', on_delete=models.CASCADE, related_name='highschools', null=True, blank=True)


class CollegeStudent(BaseStudent):
    college = models.ForeignKey(
        'College', on_delete=models.CASCADE, related_name='college_students')
    MOD_QUANTITATIVE_REASONING = models.IntegerField()
    MOD_WRITTEN_COMMUNICATION = models.IntegerField()
    MOD_CRITICAL_READING = models.IntegerField()
    MOD_ENGLISH = models.IntegerField()
    MOD_CITIZENSHIP_COMPETENCES = models.IntegerField()


class College(BaseInstitution):
    municipality = models.ForeignKey(
        'Municipality', on_delete=models.CASCADE, related_name='colleges', null=True, blank=True)


class Municipality(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, related_name='municipalities', null=True, blank=True)


class Department(models.Model):
    name = models.CharField(max_length=255)
