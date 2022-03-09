from django.db import models
from aceapi.models import AppUser, SubjectArea

class StudentSubjectArea(models.Model):
    student = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    subject_area = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)
