from django.contrib import admin

from .models import Ticket, Reply


class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'assigned_to']


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Reply)
