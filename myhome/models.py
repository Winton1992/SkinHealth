from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=500)

class UV(models.Model):
        value = models.IntegerField()
        time = models.DateTimeField(default=timezone.now)

class Temperature(models.Model):
    value = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)

class Humidity(models.Model):
    value = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)