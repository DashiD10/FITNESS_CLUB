from django.contrib import admin
from django.urls import path, include
from core.views import landing, thanks, orders_list, order_detail, create_review, create_order, get_trainer_services
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('thanks/', thanks, name='thanks'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('review/create/', create_review, name='create_review'),
    path('orders/create/', create_order, name='create_order'),
    path('api/trainer/<int:trainer_id>/services/', get_trainer_services, name='get_trainer_services'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
