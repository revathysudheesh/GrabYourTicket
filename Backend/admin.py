from django.contrib import admin

# Register your models here.
from .models import CustomUser, TheatreDB

admin.site.register(CustomUser)
admin.site.register(TheatreDB)

