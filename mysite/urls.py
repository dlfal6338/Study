# mysite/urls.py

from django.contrib import admin
from django.urls import path,re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

def custom_serve(request, path, document_root=None, show_indexes=True):
    # 보안 검증 제거
    full_path = os.path.abspath(os.path.join(document_root, path))
    return serve(request, path, document_root, show_indexes)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', include("polls.urls", namespace='polls')),
    path('main/',include("main.urls",namespace='main')),
    path('accounts/', include("accounts.urls", namespace='accounts')),
    re_path(r'^media/(?P<path>.*)$', custom_serve, {'document_root': '/'}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)