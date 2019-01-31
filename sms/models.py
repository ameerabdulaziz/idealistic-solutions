from django.db import models
from django.utils import timezone
from django.urls import reverse


class SmsGeteway(models.Model):
    name = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sms:smsgeteway_list', kwargs={'pk':self.pk})


class Template(models.Model):
    name = models.CharField(max_length=20, unique=True)
    detail = models.TextField(max_length=320,blank=True,null=True)
    active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sms:template_detail', kwargs={'pk':self.pk})


class PhoneBook(models.Model):
    name = models.CharField(max_length=25, unique=True)
    active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sms:phonebook_detail', kwargs={'pk':self.pk})


class Contact(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    country = models.CharField(max_length=25)
    phone_number = models.IntegerField()
    email = models.EmailField(max_length=25)
    company = models.CharField(max_length=25)
    phonebook = models.ForeignKey(PhoneBook,on_delete=models.SET_NULL,null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name, self.last_name

    def get_absolute_url(self):
        return reverse('sms:contact_detail', kwargs={'pk':self.pk})

    class META():
        unique_together = ('country','phone_number')




class Message(models.Model):
    phone_number = models.IntegerField()
    message = models.TextField(max_length=480)
    template = models.ForeignKey(Template,on_delete=models.SET_NULL,blank=True,null=True)
    phonenook = models.ForeignKey(PhoneBook,on_delete=models.SET_NULL,blank=True,null=True)
    smsgeteway = models.ForeignKey(SmsGeteway,on_delete=models.SET_NULL,blank=True,null=True)
    ready_to_send = models.BooleanField(default=True)
    time_to_send = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=30)
    status = models.CharField(max_length=10)
    sent = models.DateTimeField(blank=True,null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number

    def get_absolute_url(self):
        return reverse('sms:message_detail', kwargs={'pk':self.pk})
