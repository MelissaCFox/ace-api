from django.db import models
from aceapi.models import AppUser, Test

class Score(models.Model):
    student = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    date = models.DateField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    english = models.IntegerField()
    math = models.IntegerField()
    reading = models.IntegerField()
    science = models.IntegerField()

    ## add custom property to calculate overall score for test
