from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # ← LOGIN / LOGOUT / PASSWORD RESET, etc.
    path('', include('blog.urls')),  # home del sitio = app blog
]
