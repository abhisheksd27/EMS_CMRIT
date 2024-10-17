from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class IsHOD(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'HOD'

class IsPrincipal(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'PRINCIPAL'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'STUDENT'
