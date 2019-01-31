from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('contacts/', TemplateView.as_view(template_name='contacts.html'), name='contacts'),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    path('search/', include('search.urls')),
    path('service/', include('shop.urls')),
    path('tickets/', include('ticketing_system.urls')),
    path('sms/', include('sms.urls')),

    path('api/', include('api.urls', namespace='api')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api-auth/', include('rest_framework.urls')),  # To activate login option in django rest framework
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),

    path('admin/', admin.site.urls),
    # Should be last one in URL
    path('', include('static_pages.urls')),
]

if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
