from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ['email']  # Change this to order by email instead of username
    list_display = ['email', 'role', 'is_active']  # Update as needed
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'usn', 'branch')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'usn', 'branch')}),
    )

# Register the custom admin
admin.site.register(User, CustomUserAdmin)
