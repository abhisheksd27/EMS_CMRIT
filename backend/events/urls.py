# urls.py

from django.urls import path
from .views import (
    EventCreateView,
    AdminEventListView,
    AdminEditEventView,
    AdminDeleteEventView,
    HODEventApprovalView,
    PrincipalEventApprovalView,
    StudentEventListView,
    EventRegisterView,
    AdminManageRegisteredStudentsView,
    StudentRegisteredEventsView,
    StudentSubmitFeedbackView,
    AdminViewFeedbackView,
)

urlpatterns = [
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/admin/', AdminEventListView.as_view(), name='admin-event-list'),
    path('events/edit/<int:pk>/', AdminEditEventView.as_view(), name='admin-edit-event'),
    path('events/delete/<int:pk>/', AdminDeleteEventView.as_view(), name='admin-delete-event'),
    path('events/hod/approve/<int:event_id>/', HODEventApprovalView.as_view(), name='hod-event-approval'),
    path('events/principal/approve/<int:event_id>/', PrincipalEventApprovalView.as_view(), name='principal-event-approval'),
    path('events/student/', StudentEventListView.as_view(), name='student-event-list'),
    path('events/register/<int:event_id>/', EventRegisterView.as_view(), name='event-register'),
    path('events/admin/manage-students/<int:event_id>/', AdminManageRegisteredStudentsView.as_view(), name='admin-manage-registered-students'),
    path('events/student/registered/', StudentRegisteredEventsView.as_view(), name='student-registered-events'),
    path('events/feedback/submit/<int:event_id>/', StudentSubmitFeedbackView.as_view(), name='student-submit-feedback'),
    path('events/feedback/admin/<int:event_id>/', AdminViewFeedbackView.as_view(), name='admin-view-feedback'),
]
