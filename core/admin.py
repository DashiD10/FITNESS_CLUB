from django.contrib import admin
from .models import Service, Trainer, Order, Review

class TrainerAdmin(admin.ModelAdmin):
    filter_horizontal = ('services',)

    def get_changeform_initial_data(self, request):
        # Override initial data for add form to set services empty
        initial = super().get_changeform_initial_data(request)
        initial['services'] = []
        return initial

admin.site.register(Service)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Order)
admin.site.register(Review)
