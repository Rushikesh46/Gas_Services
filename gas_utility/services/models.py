from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = PhoneNumberField(region="IN")

    def __str__(self):
        return self.user.username

class ServiceRequest(models.Model):
    REQUEST_TYPES = [
        ('INSTALLATION', 'Installation'),
        ('MAINTENANCE', 'Maintenance'),
        ('REPAIR', 'Repair'),
        ('OTHER', 'Other'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='service_requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    details = models.TextField()
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_request_type_display()} - {self.customer.user.username}"

    class Meta:
        ordering = ['-submitted_at']
