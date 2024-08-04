from django.contrib import admin
from applications.home.models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id","bio","birth_date","location")
admin.site.register(Profile, ProfileAdmin)