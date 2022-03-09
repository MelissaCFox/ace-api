from django.db import models
from aceapi.models import AppUser, Test

class StudentTest(models.Model):
    student = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    english = []
    math = []
    reading = []
    science = []
