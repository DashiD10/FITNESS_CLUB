from django.contrib import admin
from django.urls import path
from core.views import landing, thanks

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='home'),
    path('thanks/', thanks, name='thanks'),
]
