from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    gender = models.CharField(max_length=6, choices=(("male",u"male"),("female",u"female"),("secret", u"secret")), default="secret")
    email = models.EmailField(null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=100, default=u"")



    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return (self.username)


# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=500)


class Seneor(models.Model):
    Tvalue = models.FloatField()
    Hvalue = models.FloatField()
    Uvalue = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)

