from django.db import models
from aceapi.models import AppUser

class TutorStudent(models.Model):
    student = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="student")
    tutor = models.ForeignKey(AppUser, on_delete=models.CASCADE)
