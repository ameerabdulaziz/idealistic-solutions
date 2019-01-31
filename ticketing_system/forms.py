from django import forms

from .models import Reply, Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'department', 'assigned_to', 'priority', 'status', 'content', 'attachments']

    # filter on logedin user and remove some files from form
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TicketForm, self).__init__(*args, **kwargs)
        login_user = self.request.user
        if not login_user.is_superuser:
            del self.fields['assigned_to']
            del self.fields['status']




class ReplayForm(forms.ModelForm):
    class Meta:
        model = Reply
        exclude = ['user', 'ticket']
