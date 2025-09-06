from django.contrib import admin
from .models import Service, Trainer, Order, Review

# Register your models here.
admin.site.register(Service)
admin.site.register(Trainer)
admin.site.register(Order)
admin.site.register(Review)
