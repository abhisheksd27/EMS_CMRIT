from rest_framework import serializers
from .models import Event
from users.models import User

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date_time', 'location', 'venue',
            'total_attendees', 'guest_names', 'main_guests', 'budget',
            'participants_limit', 'status', 'created_by', 'admin_contact_number', 'admin_email',
            'registered_students'
        ]
        read_only_fields = ['status', 'created_by', 'registered_students']

    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['created_by'] = request_user  # Attach the admin creating the event
        return super().create(validated_data)
