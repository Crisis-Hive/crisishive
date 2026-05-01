from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    division = models.CharField(max_length=100)
    population = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class GeoTag(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"