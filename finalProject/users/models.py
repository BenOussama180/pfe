from django.db import models
from datetime import datetime

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now,blank=True)
    #what to show instead of usersobject(n)
    def __str__(self):
        return self.name
    #so in the administration its not Userss
    class Meta:
        verbose_name_plural = "Users"
