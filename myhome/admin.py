from django.contrib import admin
from .models import Notification,UserProfile

# Register your models here.
admin.site.register(Notification)

class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = UserProfile


admin.site.register(UserProfile)