from django.contrib import admin

# Register your models here.
from .models import CustomUser, TheatreDB,ScreenDB

admin.site.register(CustomUser)
admin.site.register(TheatreDB)
admin.site.register(ScreenDB)

