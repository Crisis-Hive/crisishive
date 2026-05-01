from django.db import models
from accounts.models import User
from location.models import District
from feed.models import Crisis


class ResponseTeam(models.Model):
    TEAM_TYPE_CHOICES = [
        ('medical', 'Medical'),
        ('fire', 'Fire'),
        ('rescue', 'Rescue'),
        ('ngo', 'NGO'),
        ('government', 'Government'),
    ]

    name = models.CharField(max_length=255)
    team_type = models.CharField(max_length=20, choices=TEAM_TYPE_CHOICES)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='led_teams')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    contact = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    team = models.ForeignKey(ResponseTeam, on_delete=models.CASCADE, related_name='assignments')
    crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE, related_name='assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.team.name} → {self.crisis.title}"


class StatusUpdate(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('responding', 'Responding'),
        ('resolved', 'Resolved'),
    ]

    crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE, related_name='status_updates')
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    new_status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crisis.title} → {self.new_status}"

    class Meta:
        ordering = ['-created_at']
