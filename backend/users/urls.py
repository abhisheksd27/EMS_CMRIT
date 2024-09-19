from django.urls import path
from .views import AdminRegisterView, HODRegisterView, PrincipalRegisterView, StudentRegisterView
from .views import AdminLoginView, HODLoginView, PrincipalLoginView, StudentLoginView
urlpatterns = [
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('hod/register/', HODRegisterView.as_view(), name='hod-register'),
    path('principal/register/', PrincipalRegisterView.as_view(), name='principal-register'),
    path('student/register/', StudentRegisterView.as_view(), name='student-register'),
    
    
    
     path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('hod/login/', HODLoginView.as_view(), name='hod-login'),
    path('principal/login/', PrincipalLoginView.as_view(), name='principal-login'),
    path('student/login/', StudentLoginView.as_view(), name='student-login'),
]
