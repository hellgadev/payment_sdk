
from django.contrib import admin
from django.urls import path

from core.api.views import PaymentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/pay/', PaymentView.as_view())
]
