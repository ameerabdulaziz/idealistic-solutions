from django.urls import path
from sms.views import (PhoneBookCreateView,PhoneBookUpdateView,PhoneBookListView,
                        PhoneBookDetailView,PhoneBookDeleteView,PhoneBookCreateView,
                        PhoneBookUpdateView,PhoneBookListView,PhoneBookDetailView,
                        PhoneBookDeleteView,TemplateCreateView,TemplateUpdateView,
                        TemplateListView, TemplateDetailView,TemplateDeleteView,
                        ContactCreateView,ContactUpdateView,ContactListView,
                        ContactDetailView,ContactDeleteView,MessageCreateView,
                        MessageUpdateView,MessageListView, MessageDetailView,
                        MessageDeleteView,SmsGetewayCreateView,SmsGetewayUpdateView,
                        SmsGetewayListView,SmsGetewayDetailView,SmsGetewayDeleteView
                        )
app_name = 'sms'

urlpatterns = [
    path('phonebook/new/', PhoneBookCreateView.as_view(),name='phonebook_create'),
    path('phonebook/', PhoneBookListView.as_view(),name='phonebook_list'),
    path('phonebook/<int:pk>/update/', PhoneBookUpdateView.as_view(),name='phonebook_update'),
    path('phonebook/<int:pk>/delete/', PhoneBookDeleteView.as_view(),name='phonebook_delete'),
    path('phonebook/<int:pk>/', PhoneBookDetailView.as_view(),name='phonebook_detail'),

    path('message/new/', MessageCreateView.as_view(),name='message_create'),
    path('message/', MessageListView.as_view(),name='message_list'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(),name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(),name='message_delete'),
    path('message/<int:pk>/', MessageDetailView.as_view(),name='message_detail'),

    path('contact/new/', ContactCreateView.as_view(),name='contact_create'),
    path('contact/', ContactListView.as_view(),name='contact_list'),
    path('contact/<int:pk>/update/', ContactUpdateView.as_view(),name='contact_update'),
    path('contact/<int:pk>/delete/', ContactDeleteView.as_view(),name='contact_delete'),
    path('contact/<int:pk>/', ContactDetailView.as_view(),name='contact_detail'),

    path('smsgeteway/new/', SmsGetewayCreateView.as_view(),name='smsgeteway_create'),
    path('smsgeteway/', SmsGetewayListView.as_view(),name='smsgeteway_list'),
    path('smsgeteway/<int:pk>/update/', SmsGetewayUpdateView.as_view(),name='smsgeteway_update'),
    path('smsgeteway/<int:pk>/delete/', SmsGetewayDeleteView.as_view(),name='smsgeteway_delete'),
    path('smsgeteway/<int:pk>/', SmsGetewayDetailView.as_view(),name='smsgeteway_detail'),

    path('template/new/', TemplateCreateView.as_view(),name='template_create'),
    path('template/', TemplateListView.as_view(),name='template_list'),
    path('template/<int:pk>/update/', TemplateUpdateView.as_view(),name='template_update'),
    path('template/<int:pk>/delete/', TemplateDeleteView.as_view(),name='template_delete'),
    path('template/<int:pk>/', TemplateDetailView.as_view(),name='template_detail'),
]
