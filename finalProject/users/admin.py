

from django.contrib.admin.decorators import register
from .resources import UsersResource
from django.contrib import admin
from .models import Users
from import_export.admin import ImportExportModelAdmin

# Register your models here.
# admin.site.register(Users)
@admin.register(Users)

class UsersAdmin(ImportExportModelAdmin):
    list_display = ('name','prenom','email','city')

