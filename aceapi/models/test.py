from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=10)
    year = models.IntegerField()
    num_sci = models.IntegerField()


    @property
    def liked(self):
        """custom property to determine if the currently logged in user has liked a test or not"""
        return self.__favorite

    @liked.setter
    def liked(self, value):
        self.__favorite = value
