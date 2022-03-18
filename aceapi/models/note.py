from django.db import models
from aceapi.models import AppUser

class Note(models.Model):
    student = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    note = models.CharField(max_length=500)
    date = models.DateField()
    pinned = models.BooleanField()
