from django.urls import path,include
from . import views
from rest_framework import routers

app_name = 'api'
router = routers.DefaultRouter()
# router.register('post', views.Posts_Api)

urlpatterns = [
    path('', include(router.urls))
]
