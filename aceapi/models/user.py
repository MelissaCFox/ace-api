from django.db import models
from django.contrib.auth.models import User

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    billing_rate = models.FloatField(null=True, blank=True)
    day = models.ForeignKey("Day", on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    parent_name = models.CharField(null=True, max_length=50, blank=True)
    parent_email = models.EmailField(null=True, blank=True)

    focus_areas = models.ManyToManyField("SubjectArea", through="StudentSubjectArea")

##* Add profile image field (having issue with Pillow during ftf deployment?)


    @property
    def superscore(self):
        """calculate max scores (superscores) for each section"""
        return self.__superscore

    @superscore.setter
    def superscore(self,value):
        self.__superscore = value
