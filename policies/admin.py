from django.contrib import admin

from .models import Policy


class PolicyAdmin(admin.ModelAdmin):
    list_display = ['policy_id', 'customer_name', 'policy_type', 'expiry_date', 'is_expired']
    list_display_links = ['policy_id']
    list_filter = ['expiry_date', 'policy_type']
    search_fields = ['customer_name']


admin.site.register(Policy, PolicyAdmin)
