from django.db import models
from datetime import datetime


# TODO change the model name to person for example
class Person(models.Model):
    name = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    city = models.CharField(max_length=100)
    # what to show instead of usersobject(n)

    def __str__(self):
        return self.name
    # so in the administration its not Userss

    class Meta:
        verbose_name_plural = "Persones"
