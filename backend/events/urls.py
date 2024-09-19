from django.urls import path
from .views import (
    EventCreateView, AdminEventListView, AdminEditEventView, HODEventApprovalView, PrincipalEventApprovalView,
    StudentEventListView, EventRegisterView, HODDashboardView, PrincipalDashboardView
)

urlpatterns = [
    path('admin/create/', EventCreateView.as_view(), name='event-create'),
    path('admin/events/', AdminEventListView.as_view(), name='admin-event-list'),
    path('admin/edit/<int:pk>/', AdminEditEventView.as_view(), name='admin-event-edit'),
    path('hod/events/', HODEventApprovalView.as_view(), name='hod-event-list'),
    path('hod/dashboard/', HODDashboardView.as_view(), name='hod-dashboard'),
    path('principal/dashboard/', PrincipalDashboardView.as_view(), name='principal-dashboard'),
    path('student/events/', StudentEventListView.as_view(), name='student-event-list'),
    path('student/events/register/<int:event_id>/', EventRegisterView.as_view(), name='event-register'),
]
