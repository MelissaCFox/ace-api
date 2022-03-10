from django.db import models
from aceapi.models import AppUser, Test

class StudentTest(models.Model):
    student = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    english = models.CharField(max_length=20)
    math = models.CharField(max_length=20)
    reading = models.CharField(max_length=20)
    science = models.CharField(max_length=20)
