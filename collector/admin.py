from django.contrib import admin
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'preferred_technology', 'is_locked')
    list_filter = ('preferred_technology', 'is_locked')