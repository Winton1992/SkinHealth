from django.db import models


# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=500)

class UV(models.Model):
        value = models.IntegerField()
