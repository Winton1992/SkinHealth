from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user=models.OneToOneField(User)
    gender=models.CharField(max_length=10,default='')
    skinType=models.CharField(max_length=10,default='')

    def __str__(self):
        return self.user.username
#
# def create_profile(sender,**kwargs):
#     if kwargs['created']:
#         user_profile=UserProfile.objects.create(user=kwargs['instance'])
#
# post_save.connect(create_profile,sender=User)

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)

