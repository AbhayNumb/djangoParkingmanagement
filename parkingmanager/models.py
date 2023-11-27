from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class Parking(models.Model):
    parkingid = models.IntegerField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    
    def __str__(self):
        return f"Parking ID: {self.parkingid}, from_time: {self.from_time}, to_time: {self.to_time}, User: {self.user.username}"
