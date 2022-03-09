from django.db import models
from aceapi.models import AppUser, Test

class Like(models.Model):
    tutor = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
