from django.db import models


class User(models.Model):
    email = models.CharField(max_length=255, unique=True)
    hashed_password = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Account(models.Model):
    user = models.ForeignKey(
        'User', related_name='accounts', on_delete=models.CASCADE)
    provider = models.CharField(max_length=255)
    providerAccountId = models.CharField(max_length=255)

    class Meta:
        unique_together = ('provider', 'providerAccountId')
