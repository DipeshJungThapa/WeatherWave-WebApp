from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.city} on {self.date}"
