
from django.db import models
from django.contrib.auth.models import User

class Parking(models.Model):
    parkingid = models.IntegerField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    
    