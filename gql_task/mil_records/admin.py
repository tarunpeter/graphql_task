from django.contrib import admin
from .models import UserRecord

@admin.register(UserRecord)
class UserRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'created_at')
    ordering = ('name',)
