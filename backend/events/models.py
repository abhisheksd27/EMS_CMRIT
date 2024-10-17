# models.py in events folder

from django.db import models
from users.models import User  # Assuming User model is in users app

class Event(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED_BY_HOD', 'Approved by HOD'),
        ('REJECTED_BY_HOD', 'Rejected by HOD'),
        ('APPROVED_BY_PRINCIPAL', 'Approved by Principal'),
        ('REJECTED_BY_PRINCIPAL', 'Rejected by Principal'),
        ('COMPLETED', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    total_attendees = models.IntegerField()
    guest_names = models.CharField(max_length=255)
    main_guests = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    participants_limit = models.IntegerField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    hod = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hod_events', null=True, blank=True)
    principal = models.ForeignKey(User, on_delete=models.CASCADE, related_name='principal_events', null=True, blank=True)
    admin_contact_number = models.CharField(max_length=15)
    admin_email = models.EmailField()
    feedback_sent = models.BooleanField(default=False)  # New field

    def __str__(self):
        return self.title


class RegisteredStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registered_students_details')
    usn = models.CharField(max_length=15)  # Add field for USN
    college_email = models.EmailField()  # Add field for college email

    def __str__(self):
        return f'{self.user.email} registered for {self.event.title}'


class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedbacks')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.student.email} for {self.event.title}"


class DecisionLog(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='decision_logs')
    decision_by = models.ForeignKey(User, on_delete=models.CASCADE)
    decision = models.CharField(max_length=50)  # "Approved", "Rejected", "Held"
    decision_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.decision} by {self.decision_by.email} on {self.event.title}'
