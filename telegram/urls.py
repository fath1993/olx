from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.webhooks.views import Webhook

app_name = 'webhooks'

urlpatterns = [
    path('webhook/', csrf_exempt(Webhook.as_view()), name='webhook'),
]
