from django import forms
from sms.models import Contact,Message,PhoneBook,Template,PhoneBook,SmsGeteway


class PhoneBookForm(forms.ModelForm):

    class Meta():
        model = PhoneBook
        # exclude = ['slug']
        fields = '__all__'


class MessageForm(forms.ModelForm):

    class Meta():
        model = Message
        # exclude = ['slug']
        fields = '__all__'


class ContactForm(forms.ModelForm):

    class Meta():
        model = Contact
        # exclude = ['slug']
        fields = '__all__'


class SmsGetewayForm(forms.ModelForm):

    class Meta():
        model = SmsGeteway
        # exclude = ['slug']
        fields = '__all__'



class TemplateForm(forms.ModelForm):

    class Meta():
        model = Template
        # exclude = ['slug']
        fields = '__all__'
