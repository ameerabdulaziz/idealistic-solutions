from django.urls import path

from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.TicketListView.as_view(), name='list'),
    path('create/', views.TicketCreateView.as_view(), name='create'),
    path('<int:pk>/reply/create/', views.ReplayCreateView.as_view(), name='create-reply'),
    path('<int:pk>/', views.TicketDetail.as_view(), name='detail'),
    path('<int:pk>/edit', views.TicketUpdateView.as_view(), name='update'),
    path('<int:pk>/reopen', views.TicketreopenView, name='reopen'),
    path('<int:pk>/close', views.TicketcloseView, name='close'),
    path('<int:pk>/delete', views.TicketDeleteView.as_view(), name='delete'),
]
