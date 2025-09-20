from django.contrib import admin
from django.urls import path, include
from core.views import (
    LandingView, ThanksView, OrdersListView, OrderDetailView,
    ReviewCreateView, OrderCreateView, get_trainer_services
)
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingView.as_view(), name='landing'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('review/create/', ReviewCreateView.as_view(), name='create_review'),
    path('orders/create/', OrderCreateView.as_view(), name='create_order'),
    path('api/trainer/<int:trainer_id>/services/', get_trainer_services, name='get_trainer_services'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
