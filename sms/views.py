from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from sms.models import Contact,Message,SmsGeteway,Template,PhoneBook
from sms.forms import PhoneBookForm,MessageForm,ContactForm,SmsGetewayForm,TemplateForm


###################################PhoneBook###################################
class PhoneBookCreateView(LoginRequiredMixin,generic.CreateView):
    model = PhoneBook
    REDIRECT_FIELD_NAME = 'sms:PhoneBook_create'
    form_class = PhoneBookForm


class PhoneBookUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = PhoneBook
    form_class = PhoneBookForm


class PhoneBookListView(LoginRequiredMixin,generic.ListView):
    paginate_by = 20
    model = PhoneBook

    def get_queryset(self):
        return PhoneBook.objects.all()


class PhoneBookDetailView(LoginRequiredMixin,generic.DetailView):
    model = PhoneBook


class PhoneBookDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = PhoneBook
    success_url = reverse_lazy('sms:phonebook_list')

###################################Message###################################
class MessageCreateView(LoginRequiredMixin,generic.CreateView):
    model = Message
    REDIRECT_FIELD_NAME = 'sms:Message_create'
    form_class = MessageForm


class MessageUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Message
    form_class = MessageForm


class MessageListView(LoginRequiredMixin,generic.ListView):
    paginate_by = 20
    model = Message

    def get_queryset(self):
        return Message.objects.all()


class MessageDetailView(LoginRequiredMixin,generic.DetailView):
    model = Message


class MessageDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Message
    success_url = reverse_lazy('sms:Message_list')

###################################Contact###################################
class ContactCreateView(LoginRequiredMixin,generic.CreateView):
    model = Contact
    REDIRECT_FIELD_NAME = 'sms:Contact_create'
    form_class = ContactForm


class ContactUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Contact
    form_class = ContactForm


class ContactListView(LoginRequiredMixin,generic.ListView):
    paginate_by = 20
    model = Contact

    def get_queryset(self):
        return Contact.objects.all()


class ContactDetailView(LoginRequiredMixin,generic.DetailView):
    model = Contact


class ContactDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Contact
    success_url = reverse_lazy('sms:Contact_list')

###################################SmsGeteway###################################
class SmsGetewayCreateView(LoginRequiredMixin,generic.CreateView):
    model = SmsGeteway
    REDIRECT_FIELD_NAME = 'sms:SmsGeteway_create'
    form_class = SmsGetewayForm


class SmsGetewayUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = SmsGeteway
    form_class = SmsGetewayForm


class SmsGetewayListView(LoginRequiredMixin,generic.ListView):
    paginate_by = 20
    model = SmsGeteway

    def get_queryset(self):
        return SmsGeteway.objects.all()


class SmsGetewayDetailView(LoginRequiredMixin,generic.DetailView):
    model = SmsGeteway


class SmsGetewayDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = SmsGeteway
    success_url = reverse_lazy('sms:SmsGeteway_list')

###################################Template###################################
class TemplateCreateView(LoginRequiredMixin,generic.CreateView):
    model = Template
    REDIRECT_FIELD_NAME = 'sms:Template_create'
    form_class = TemplateForm


class TemplateUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Template
    form_class = TemplateForm


class TemplateListView(LoginRequiredMixin,generic.ListView):
    paginate_by = 20
    model = Template

    def get_queryset(self):
        return Template.objects.all()


class TemplateDetailView(LoginRequiredMixin,generic.DetailView):
    model = Template


class TemplateDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Template
    success_url = reverse_lazy('sms:Template_list')
