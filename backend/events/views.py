from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event, DecisionLog
from .serializers import EventSerializer
from users.models import User


# Admin: Create Event
class EventCreateView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save event with the current admin user as the creator
        serializer.save(created_by=self.request.user)


# Admin: List Created Events
class AdminEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only events created by the current admin
        return Event.objects.filter(created_by=self.request.user)


# Admin: Edit and Resubmit Event
class AdminEditEventView(generics.RetrieveUpdateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Admin can only edit events that they created and were rejected
        return Event.objects.filter(created_by=self.request.user, status__in=['REJECTED_BY_HOD', 'REJECTED_BY_PRINCIPAL'])

    def perform_update(self, serializer):
        # Reset the status when resubmitting the event
        serializer.save(status='PENDING')


# HOD: View and Approve/Reject Events
class HODEventApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        hod = request.user
        event = Event.objects.get(id=event_id, created_by__branch=hod.branch)
        action = request.data.get('action')  # "approve", "reject", or "hold"

        if action == 'approve':
            event.status = 'APPROVED_BY_HOD'
            decision = "Approved"
        elif action == 'reject':
            event.status = 'REJECTED_BY_HOD'
            decision = "Rejected"
        else:
            event.status = 'PENDING'
            decision = "Held"

        event.save()

        # Log the decision
        DecisionLog.objects.create(event=event, decision_by=hod, decision=decision)

        return Response({"status": event.status}, status=status.HTTP_200_OK)


# Principal: View and Approve/Reject Events
class PrincipalEventApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        principal = request.user
        event = Event.objects.get(id=event_id, status='APPROVED_BY_HOD')
        action = request.data.get('action')  # "approve", "reject", or "hold"

        if action == 'approve':
            event.status = 'APPROVED_BY_PRINCIPAL'
            decision = "Approved"
        elif action == 'reject':
            event.status = 'REJECTED_BY_PRINCIPAL'
            decision = "Rejected"
        else:
            event.status = 'PENDING'
            decision = "Held"

        event.save()

        # Log the decision
        DecisionLog.objects.create(event=event, decision_by=principal, decision=decision)

        return Response({"status": event.status}, status=status.HTTP_200_OK)


# Student: View Events and Register
class StudentEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student = self.request.user
        # Fetch events approved by Principal for the student's branch
        return Event.objects.filter(status='APPROVED_BY_PRINCIPAL', created_by__branch=student.branch)


class EventRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id, status='APPROVED_BY_PRINCIPAL')
        event.registered_students.add(request.user)
        return Response({"message": "Successfully registered for the event"}, status=status.HTTP_200_OK)


# HOD: Dashboard View (View Events by Branch)
class HODDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hod = request.user
        # Fetch events created by admin of the same branch, pending approval
        branch_events = Event.objects.filter(created_by__branch=hod.branch, status='PENDING')

        # Fetch rejected events for HOD's reference
        rejected_events = Event.objects.filter(created_by__branch=hod.branch, status='REJECTED_BY_HOD')

        data = {
            "pending_approval_events": EventSerializer(branch_events, many=True).data,
            "rejected_events": EventSerializer(rejected_events, many=True).data,
        }

        return Response(data, status=status.HTTP_200_OK)


# Principal: Dashboard View (View HOD Approved Events)
class PrincipalDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all events approved by HOD and awaiting Principal's decision
        hod_approved_events = Event.objects.filter(status='APPROVED_BY_HOD')

        data = {
            "hod_approved_events": EventSerializer(hod_approved_events, many=True).data,
        }

        return Response(data, status=status.HTTP_200_OK)
