from django.db import models
from aceapi.models import AppUser, Test

class Score(models.Model):
    student = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    date = models.DateField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    english = models.IntegerField(null=True, blank=True)
    math = models.IntegerField(null=True, blank=True)
    reading = models.IntegerField(null=True, blank=True)
    science = models.IntegerField(null=True, blank=True)

    ## add custom property to calculate overall score for test
    @property
    def overall(self):
        """if calculate overall score"""
        if self.english and self.math and self.reading and self.science:
            total = self.english + self.math + self.reading + self.science
            return total / 4
        else:
            return "N/A"
