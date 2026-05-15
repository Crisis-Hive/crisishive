from django.db import models
from accounts.models import User
from feed.models import Crisis

class Volunteer(models.Model):
    SKILL_CHOICES = [
        ('medical', 'Medical Support'),
        ('driving', 'Driving/Transport'),
        ('food', 'Food/Water Distribution'),
        ('logistics', 'Logistics/Coordination'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='volunteer_actions')
    crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE, related_name='volunteers')
    skill = models.CharField(max_length=20, choices=SKILL_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    signed_up_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.crisis.title}"

class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    resource = models.CharField(max_length=255, blank=True) # e.g., "10 blankets"
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation for {self.crisis.title}"
