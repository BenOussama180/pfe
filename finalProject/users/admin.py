from django.contrib.admin.decorators import register
from .resources import PersonResource
from django.contrib import admin
from .models import Person
from import_export.admin import ImportExportModelAdmin

# Register your models here.
# admin.site.register(Users)
@admin.register(Person)

class UsersAdmin(ImportExportModelAdmin):
    list_display = ('name','prenom','email','city')

