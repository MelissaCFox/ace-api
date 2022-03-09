from django.db import models
from django.contrib.auth.models import User

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    billing_rate = models.FloatField()
    day = models.ForeignKey("Day", on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    parent_name = models.CharField(max_length=50)
    parent_email = models.EmailField()
    
    focus_areas = models.ManyToManyField("SubjectArea", through="StudentSubjectArea")

##* Add profile image field (having issue with Pillow during ftf deployment?)

##* custom property for superscore
