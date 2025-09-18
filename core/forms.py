from django import forms
from .models import Review, Order, Trainer, Service

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, 'Очень плохо'),
        (2, 'Плохо'),
        (3, 'Удовлетворительно'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, label="Оценка")

    class Meta:
        model = Review
        fields = ['trainer', 'rating', 'client_name', 'text']
        labels = {
            'trainer': 'Тренер',
            'client_name': 'Имя клиента',
            'text': 'Текст отзыва',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['trainer', 'services', 'name', 'phone', 'comment', 'appointment_date']
        labels = {
            'trainer': 'Тренер',
            'services': 'Услуги',
            'name': 'Имя клиента',
            'phone': 'Телефон',
            'comment': 'Комментарий',
            'appointment_date': 'Дата и время записи',
        }
        widgets = {
            'services': forms.SelectMultiple(attrs={'size': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If trainer is selected, filter services
        trainer = self.initial.get('trainer') or (self.instance.trainer if self.instance.pk else None)
        if trainer:
            self.fields['services'].queryset = trainer.services.all()
        else:
            self.fields['services'].queryset = Service.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        trainer = cleaned_data.get('trainer')
        services = cleaned_data.get('services')
        if trainer and services:
            trainer_services = set(trainer.services.values_list('id', flat=True))
            selected_services = set(service.id for service in services)
            if not selected_services.issubset(trainer_services):
                raise forms.ValidationError(f"Тренер {trainer.name} не предоставляет выбранные услуги.")
        return cleaned_data
