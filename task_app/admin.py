from django.contrib import admin
from .models import Urls


# Register your models here.
@admin.register(Urls)
class UrlAdmin(admin.ModelAdmin):
    pass
