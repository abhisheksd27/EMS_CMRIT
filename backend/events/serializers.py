from rest_framework import serializers
from .models import Event, RegisteredStudent, Feedback
from users.models import User

class RegisteredStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredStudent
        fields = ['user', 'event', 'usn', 'college_email']

class EventSerializer(serializers.ModelSerializer):
    registered_students_details = RegisteredStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date_time', 'location', 'venue',
            'total_attendees', 'guest_names', 'main_guests', 'budget',
            'participants_limit', 'status', 'created_by', 'admin_contact_number', 'admin_email',
            'registered_students_details'  # Show registered students in event details
        ]
        read_only_fields = ['status', 'created_by', 'registered_students_details']

    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['created_by'] = request_user  # Attach the admin creating the event
        return super().create(validated_data)


class RegisteredStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredStudent
        fields = '__all__'  

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['event', 'student', 'feedback_text', 'submitted_at']