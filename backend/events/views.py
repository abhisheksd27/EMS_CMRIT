from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event, RegisteredStudent, DecisionLog, Feedback
from .serializers import EventSerializer, FeedbackSerializer, RegisteredStudentSerializer
from users.models import User
from .permissions import IsAdmin, IsHOD, IsPrincipal, IsStudent

class EventCreateView(APIView):
    """
    API View for creating events (accessible only to Admin).
    """
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Ensure the creator is set
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admin: List Created Events
class AdminEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        # Return only events created by the current admin
        return Event.objects.filter(created_by=self.request.user)


# Admin: Edit and Resubmit Event
class AdminEditEventView(generics.RetrieveUpdateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        # Admin can only edit events that they created and were rejected
        return Event.objects.filter(created_by=self.request.user, status__in=['REJECTED_BY_HOD', 'REJECTED_BY_PRINCIPAL'])

    def perform_update(self, serializer):
        # Reset the status when resubmitting the event
        serializer.save(status='PENDING')


# Admin: Delete Event
class AdminDeleteEventView(generics.DestroyAPIView):
    permission_classes = [IsAdmin]

    def get_queryset(self):
        # Admin can only delete events that they created
        return Event.objects.filter(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # Get the event object
        event = self.get_object()
        # Delete the event
        event.delete()
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# HOD: View and Approve/Reject Events
class HODEventApprovalView(APIView):
    permission_classes = [IsHOD]

    def post(self, request, event_id):
        try:
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
                event.status = 'HOLD'
                decision = "Held"

            event.save()

            # Log the decision
            DecisionLog.objects.create(event=event, decision_by=hod, decision=decision)

            return Response({"status": event.status}, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)


# Principal: View and Approve/Reject Events
class PrincipalEventApprovalView(APIView):
    permission_classes = [IsPrincipal]

    def post(self, request, event_id):
        try:
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
                event.status = 'HOLD'
                decision = "Held"

            event.save()

            # Log the decision
            DecisionLog.objects.create(event=event, decision_by=principal, decision=decision)

            return Response({"status": event.status}, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)


# Student: View Events and Register
class StudentEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        student = self.request.user
        # Fetch events approved by Principal for the student's branch
        return Event.objects.filter(status='APPROVED_BY_PRINCIPAL', created_by__branch=student.branch)


class EventRegisterView(APIView):
    permission_classes = [IsStudent]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id, status='APPROVED_BY_PRINCIPAL')
            usn = request.data.get('usn')
            college_email = request.data.get('college_email')

            if event.registered_students_details.count() < event.participants_limit:
                registered_student = RegisteredStudent.objects.create(
                    user=request.user,
                    event=event,
                    usn=usn,
                    college_email=college_email
                )
                return Response({"message": "Successfully registered for the event", "usn": registered_student.usn}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Event is full"}, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            return Response({"error": "Event not found or not approved"}, status=status.HTTP_404_NOT_FOUND)


# Admin: Manage Registered Students
class AdminManageRegisteredStudentsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, event_id):
        # Get registered students for a specific event
        try:
            event = Event.objects.get(id=event_id)
            registered_students = event.registered_students_details.all()
            data = RegisteredStudentSerializer(registered_students, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, event_id, student_id):
        # Admin can delete a registered student from an event
        try:
            registered_student = RegisteredStudent.objects.get(id=student_id, event_id=event_id)
            registered_student.delete()
            return Response({"message": "Student registration deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except RegisteredStudent.DoesNotExist:
            return Response({"error": "Registered student not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, event_id):
        # Admin can add a student to an event
        usn = request.data.get('usn')
        college_email = request.data.get('college_email')
        
        try:
            user = User.objects.get(email=college_email)  # Assuming you are matching by college email
            RegisteredStudent.objects.create(user=user, event_id=event_id, usn=usn, college_email=college_email)
            return Response({"message": "Student registered successfully"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Student: View Registered Events
class StudentRegisteredEventsView(generics.ListAPIView):
    serializer_class = RegisteredStudentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        student = self.request.user
        return RegisteredStudent.objects.filter(user=student)


# Student: Submit Feedback
class StudentSubmitFeedbackView(APIView):
    permission_classes = [IsStudent]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            feedback_text = request.data.get('feedback_text')

            # Create feedback entry
            feedback = Feedback.objects.create(event=event, student=request.user, feedback_text=feedback_text)
            return Response({"message": "Feedback submitted successfully."}, status=status.HTTP_201_CREATED)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)


# Admin: View Feedback
class AdminViewFeedbackView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            feedbacks = event.feedbacks.all()  # Get feedbacks related to the event
            serializer = FeedbackSerializer(feedbacks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
