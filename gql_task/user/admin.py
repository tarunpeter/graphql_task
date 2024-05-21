from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','first_name','last_name','is_active')
    ordering = ('first_name',)
    fieldsets = (
        (_('User Details'), {
            'fields': (('first_name', 'last_name'), 'email', ('username','password'), ('is_active', 'is_staff'))
        }),
        (_('Additional Details'), {
            'fields': ('is_superuser', 'groups', 'user_permissions', 'date_joined', 'last_login',),
        }),
    )
