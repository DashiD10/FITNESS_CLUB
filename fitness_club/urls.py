from django.contrib import admin
from django.urls import path, include
from core.views import landing, thanks, orders_list, order_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('thanks/', thanks, name='thanks'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
]
