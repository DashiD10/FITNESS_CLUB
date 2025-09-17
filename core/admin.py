from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
from .models import Service, Trainer, Order, Review


class DateRangeFilter(SimpleListFilter):
    title = _('Дата записи')
    parameter_name = 'appointment_date'

    def lookups(self, request, model_admin):
        return [
            ('today', _('Сегодня')),
            ('tomorrow', _('Завтра')),
            ('this_week', _('На этой неделе')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'today':
            today = timezone.now().date()
            return queryset.filter(appointment_date__date=today)
        if self.value() == 'tomorrow':
            tomorrow = timezone.now().date() + timedelta(days=1)
            return queryset.filter(appointment_date__date=tomorrow)
        if self.value() == 'this_week':
            start_of_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(appointment_date__date__range=(start_of_week, end_of_week))


class OrderServiceInline(admin.StackedInline):
    model = Order.services.through
    extra = 0
    verbose_name = "Услуга"
    verbose_name_plural = "Услуги"


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0
    verbose_name = "Отзыв"
    verbose_name_plural = "Отзывы"


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'trainer', 'status', 'appointment_date', 'total_price')
    list_filter = ('status', 'trainer', DateRangeFilter)
    search_fields = ('name', 'phone')
    list_editable = ('status',)
    inlines = [OrderServiceInline]
    actions = ['make_approved', 'make_cancelled', 'make_in_progress', 'make_completed']

    def total_price(self, obj):
        return sum(service.price for service in obj.services.all())
    total_price.short_description = "Общая стоимость"

    def make_approved(self, request, queryset):
        queryset.update(status='approved')
    make_approved.short_description = "Подтвердить выбранные заказы"

    def make_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    make_cancelled.short_description = "Отменить выбранные заказы"

    def make_in_progress(self, request, queryset):
        queryset.update(status='in_progress')  # Note: STATUS_CHOICES has 'completed', but task says 'В работе', assuming 'approved' or add to choices
    make_in_progress.short_description = "Пометить как 'В работе'"

    def make_completed(self, request, queryset):
        queryset.update(status='completed')
    make_completed.short_description = "Завершить выбранные заказы"


class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'is_active', 'services_count')
    list_filter = ('is_active', 'services')
    search_fields = ('name',)
    filter_horizontal = ('services',)
    inlines = [ReviewInline]

    def services_count(self, obj):
        return obj.services.count()
    services_count.short_description = "Количество услуг"

    def get_changeform_initial_data(self, request):
        # Override initial data for add form to set services empty
        initial = super().get_changeform_initial_data(request)
        initial['services'] = []
        return initial


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name',)


admin.site.register(Service, ServiceAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
