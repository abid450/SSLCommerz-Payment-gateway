"""
URL configuration for sl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Payment.views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'api', PaymentViewSet, basename='paymentapi')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/checkout/', CheckoutPageView.as_view(), name='checkout'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/failed/', PaymentFailedView.as_view(), name='payment_failed'),
    path('payment/cancelled/', PaymentCancelledView.as_view(), name='payment_cancelled'),
    path('payment/ipn/', PaymentIPNView.as_view(), name='payment_ipn'),
    path('payment/api/initiate/', payment_initiate, name='payment_initiate'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)