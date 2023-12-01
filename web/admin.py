from django.contrib import admin
from web.models import Contact


# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name","email","subject","message")
    

