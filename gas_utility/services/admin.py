from django.contrib import admin
from .models import Customer, ServiceRequest

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone')
    search_fields = ('user__username', 'user__email', 'address', 'phone')

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('customer', 'request_type', 'status', 'submitted_at', 'resolved_at')
    list_filter = ('request_type', 'status', 'submitted_at', 'resolved_at')
    search_fields = ('customer__user__username', 'customer__user__email', 'details')
    date_hierarchy = 'submitted_at'
    ordering = ('-submitted_at',)
    fieldsets = (
        (None, {
            'fields': ('customer', 'request_type', 'details', 'attachment')
        }),
        ('Status and Resolution', {
            'fields': ('status', 'submitted_at', 'resolved_at')
        }),
    )

admin.site.register(Customer, CustomerAdmin)
admin.site.register(ServiceRequest, ServiceRequestAdmin)
