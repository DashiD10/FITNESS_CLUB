from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Order
from .telegram import send_telegram_message


@receiver(m2m_changed, sender=Order.services.through)
def notify_new_order(sender, instance, action, **kwargs):
    """
    Send Telegram notification when services are added to an Order.
    """
    if action == 'post_add':
        # Form the message
        trainer_name = instance.trainer.name if instance.trainer else 'Не указан'
        services_list = ', '.join([service.name for service in instance.services.all()])
        appointment_date = instance.appointment_date.strftime('%d.%m.%Y %H:%M')

        message = (
            f"*Новая запись!*\n\n"
            f"*Имя клиента:* {instance.name}\n"
            f"*Телефон:* {instance.phone}\n"
            f"*Тренер:* {trainer_name}\n"
            f"*Услуги:* {services_list}\n"
            f"*Дата записи:* {appointment_date}"
        )

        # Send the message
        send_telegram_message(message)
