from django.db import models
from accounts.models import User
from location.models import District, GeoTag


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)   # emoji or icon slug
    color = models.CharField(max_length=7, blank=True)   # hex e.g. #FF0000

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Crisis(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('responding', 'Responding'),
        ('resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_crises')
    geotag = models.ForeignKey(GeoTag, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ongoing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Crises"


class CrisisMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='crisis_media/')
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} for {self.crisis.title}"


class Upvote(models.Model):
    crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE, related_name='upvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('crisis', 'user')

    def __str__(self):
        return f"{self.user.email} upvoted {self.crisis.title}"
