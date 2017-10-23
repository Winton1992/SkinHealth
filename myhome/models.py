from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=500)


class Seneor(models.Model):
    Tvalue = models.FloatField()
    Hvalue = models.FloatField()
    Uvalue = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)

