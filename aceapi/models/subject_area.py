from django.db import models
from aceapi.models import Subject

class SubjectArea(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
