from django.db import models

STATUS_CHOICES = [
    ('not_approved', 'Не одобрен'),
    ('approved', 'Одобрен'),
    ('completed', 'Завершен'),
    ('cancelled', 'Отменен'),
]

RATING_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
]

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Программа тренировок")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность", help_text="Время тренировки")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="services/", blank=True, verbose_name="Изображение")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Trainer(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(upload_to="trainers/", blank=True, verbose_name="Фотография")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")
    services = models.ManyToManyField(Service, related_name="trainers", verbose_name="Услуги")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"


class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="not_approved", verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, verbose_name="Тренер")
    services = models.ManyToManyField(Service, related_name="orders", verbose_name="Услуги")
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")

    def __str__(self):
        return f"Заказ от {self.name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, verbose_name="Тренер")
    photo = models.ImageField(upload_to="reviews/", blank=True, null=True, verbose_name="Фотография")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")

    def __str__(self):
        return f"Отзыв от {self.client_name or 'Аноним'}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
