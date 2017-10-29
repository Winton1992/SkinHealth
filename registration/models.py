from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user=models.OneToOneField(User)
    GENDER_CHOICE=(
        ('femail','femail'),
        ('male','male'),
    )

    SKINTYPE_CHOICE = (
        ('dry', 'dry'),
        ('oily', 'oily'),
        ('q','normal'),
    )
    gender=models.CharField(max_length=10,default='',choices=GENDER_CHOICE)
    skinType=models.CharField(max_length=10,default='',choices=SKINTYPE_CHOICE)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)

