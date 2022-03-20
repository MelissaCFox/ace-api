from django.db import models
from aceapi.models import AppUser, Test

class StudentTest(models.Model):
    student = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    english = models.CharField(max_length=20)
    math = models.CharField(max_length=20)
    reading = models.CharField(max_length=20)
    science = models.CharField(max_length=20)

    @property
    def completion(self):
        """percentage completion for science passages"""
        english = 0
        for passage in self.english.split(","):
            if passage == "1":
                english += 1
        english = round(english / 5, 2)

        math = 0
        for passage in self.math.split(","):
            if passage == "1":
                math += 1
        math = round(math / 3, 2)

        reading = 0
        for passage in self.reading.split(","):
            if passage == "1":
                reading += 1
        reading = reading / 4

        science = 0
        for passage in self.science.split(","):
            if passage == "1":
                science += 1
        science = round(science / len(self.science.split(",")), 2)

        return {
            "english": english,
            "math": math,
            "reading": reading,
            "science": science,
            "overall": round((english + math + reading + science) /4, 2)
            }
