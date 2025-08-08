from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Library Info', {'fields': ('penalty_points',)}),
    )
    list_display = UserAdmin.list_display + ('penalty_points',)
    list_filter = UserAdmin.list_filter + ('penalty_points',)

admin.site.register(User, CustomUserAdmin)
