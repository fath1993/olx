from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from olx import settings

def redirect_to_admin_view(request):
    return redirect('/admin/')


urlpatterns = [
    path("admin/", admin.site.urls, name='admin'),
    path("", redirect_to_admin_view),
]
# test
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
