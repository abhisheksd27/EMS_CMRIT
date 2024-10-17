# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ['email']
    list_display = ['email', 'role', 'is_active']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'usn', 'branch')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'usn', 'branch')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Optionally, filter users based on the role of the logged-in admin
        if request.user.role != 'ADMIN':
            return qs.exclude(role='ADMIN')  # Example: non-admins can't see admin users
        return qs

# Register the custom admin
# admin.site.register(User, CustomUserAdmin)
#