from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=10)
    year = models.IntegerField()
    num_sci = models.IntegerField()

##* custom "liked" property
