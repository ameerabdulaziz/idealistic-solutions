from django.contrib import admin
from sms.models import Contact,Message,SmsGeteway,Template,PhoneBook

admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(SmsGeteway)
admin.site.register(Template)
admin.site.register(PhoneBook)
