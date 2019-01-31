from django.urls import path
from static_pages import views

app_name = 'static_pages'


urlpatterns=[
    path('static_pages/new/', views.StaticPagesCreateView.as_view(),name='static_pages_create'),
    path('static_pages/list/', views.StaticPagesListView.as_view(),name='static_pages_list'),
    path('static_pages/<slug>/update/', views.StaticPagesupdateView.as_view(),name='static_pages_update'),
    path('static_pages/<slug>/delete/', views.StaticPagesDeleteView.as_view(),name='static_pages_delete'),
    path('<slug>/', views.StaticPagesDetailView.as_view(),name='static_pages_detail'),
    ]
